from flask import Blueprint, request, jsonify
from .models import User, ParkingSlot, Booking, Payment, db
from .schemas import CheckAvailabilitySchema, BookSlotSchema, ProcessPaymentSchema
from marshmallow import ValidationError

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/check-availability', methods=['POST'])
def check_availability():
    try:
        data = CheckAvailabilitySchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    date = data['date']
    time = data['time']
    vehicle_type = data['vehicle_type']

    # Fetch available slots
    booked_slots = db.session.query(Booking.slot_id).filter_by(date=date, time=time).all()
    booked_slot_ids = [slot[0] for slot in booked_slots]

    available_slots = ParkingSlot.query.filter(
        ParkingSlot.vehicle_type == vehicle_type,
        ParkingSlot.is_available == True,
        ~ParkingSlot.id.in_(booked_slot_ids)
    ).all()

    slots = [{"slot_id": slot.slot_id, "vehicle_type": slot.vehicle_type} for slot in available_slots]

    return jsonify({"slots": slots})

@api_bp.route('/api/book-slot', methods=['POST'])
def book_slot():
    try:
        data = BookSlotSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Create or fetch user
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()

    # Fetch the selected slot
    slot = ParkingSlot.query.filter_by(slot_id=data['slot_id']).first()
    if not slot:
        return jsonify({"error": "Slot does not exist"}), 404
    if not slot.is_available:
        return jsonify({"error": "Slot is already booked"}), 400

    # Create booking
    try:
        booking = Booking(user_id=user.id, slot_id=slot.id, date=data['date'], time=data['time'])
        db.session.add(booking)
        slot.is_available = False  # Mark slot as booked
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"Slot {data['slot_id']} booked for {data['name']}", "bookingId": booking.id})

@api_bp.route('/api/process-payment', methods=['POST'])
def process_payment():
    try:
        data = ProcessPaymentSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Fetch the booking to validate it
    booking = Booking.query.filter_by(id=data['booking_id']).first()
    if not booking:
        return jsonify({"error": "Invalid booking ID"}), 404

    # Check if payment already exists for this booking
    existing_payment = Payment.query.filter_by(booking_id=data['booking_id']).first()
    if existing_payment:
        return jsonify({"error": "Payment already processed for this booking"}), 400

    # Mock payment processing
    try:
        payment = Payment(booking_id=data['booking_id'], amount=10.0, status="Success")
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Payment successful"})                        
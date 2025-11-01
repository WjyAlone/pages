from models import Message, db

class MessageService:
    @staticmethod
    def create_message(name, email, message):
        user = Message(name=name, email=email, message=message)
        db.session.add(user)
        db.session.commit()
        return user
    @staticmethod
    def get_messages():
        return Message.query.all()
    @staticmethod
    def delete_message(id):
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return id

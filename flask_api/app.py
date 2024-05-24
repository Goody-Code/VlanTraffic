from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vlan_data.db'
db = SQLAlchemy(app)

class VLANData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.String(50))
    vlan_name = db.Column(db.String(50))
    vlan_id = db.Column(db.Integer)
    vlan_interface = db.Column(db.String(50))
    rx_bytes = db.Column(db.Integer)
    tx_bytes = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class VLANNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vlan_name = db.Column(db.String(50), unique=True)
    note = db.Column(db.String(200))

@app.route('/vlan_data', methods=['POST'])
def vlan_data():
    data = request.json
    router_id = data['router_id']
    for vlan in data['vlans']:
        vlan_entry = VLANData(
            router_id=router_id,
            vlan_name=vlan['name'],
            vlan_id=vlan['id'],
            vlan_interface=vlan['interface'],
            rx_bytes=vlan['rxBytes'],
            tx_bytes=vlan['txBytes']
        )
        db.session.add(vlan_entry)
    db.session.commit()
    return jsonify({'message': 'Data received'}), 200

@app.route('/vlan_note', methods=['POST'])
def vlan_note():
    data = request.json
    vlan_name = data['vlan_name']
    note = data['note']
    existing_note = VLANNote.query.filter_by(vlan_name=vlan_name).first()
    if existing_note:
        existing_note.note = note
    else:
        new_note = VLANNote(vlan_name=vlan_name, note=note)
        db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note saved'}), 200

def generate_report(period):
    end_date = datetime.utcnow()
    if period == 'daily':
        start_date = end_date - timedelta(days=1)
    elif period == 'weekly':
        start_date = end_date - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = end_date - timedelta(days=30)
    else:
        return None

    data = VLANData.query.filter(VLANData.timestamp >= start_date).all()
    notes = VLANNote.query.all()
    notes_dict = {note.vlan_name: note.note for note in notes}

    report_data = []
    for vlan in data:
        note = notes_dict.get(vlan.vlan_name, "")
        report_data.append({
            'name': vlan.vlan_name,
            'rx_bytes': vlan.rx_bytes,
            'tx_bytes': vlan.tx_bytes,
            'note': note
        })

    df = pd.DataFrame(report_data)
    plt.figure(figsize=(10, 6))
    plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    plt.axis('off')

    report_filename = f'report_{period}.png'
    plt.savefig(report_filename)
    plt.close()

    return report_filename

def send_telegram_report(period, bot_token, chat_id):
    report_filename = generate_report(period)
    if report_filename:
        import telegram
        bot = telegram.Bot(token=bot_token)
        with open(report_filename, 'rb') as report_file:
            bot.send_photo(chat_id=chat_id, photo=report_file, caption=f'{period.capitalize()} VLAN Usage Report')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)

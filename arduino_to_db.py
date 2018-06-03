import serial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# Decodes a {bytes string} and split the input into list
def decode_string(byte_string):
    return byte_string.decode("utf-8").split()


# Loads a {list} to a specified {table} in db
def list_to_table(data_list, table, sess):
    temp = float(data_list[0])
    press = float(data_list[1])
    alt = float(data_list[2])

    sess.execute("INSERT INTO {}(Temperature, Pressure, ApproxAlt)"
                 "VALUES({},{},{})".format(table, temp, press, alt))
    sess.flush()
    sess.commit()
    print('Row added!')


engine = create_engine("mysql://<user_name>:<password>@<host_name>/smsmagic")
session_obj = sessionmaker(bind=engine)
session = scoped_session(session_obj)

# Create table to load the data in
# If you already have a table, don't run this
session.execute(
    "CREATE TABLE arduino_data(id INTEGER PRIMARY KEY, Temperature FLOAT, "
    "Pressure FLOAT, ApproxAlt Float)"
                )
session.flush()

# Get the data from Arduino and load them to db
ser = serial.Serial('COM3', 9600)
while True:
    x = decode_string(ser.readline())
    list_to_table(x, 'arduino_data', session)


# Test strings
# s1 = b'33.79 98332.80 252.15 \r\n'
# s2 = b'34.79 59332.80 275.15 \r\n'
# list_to_table(decode_string(s1), 'arduino_data', session)
# list_to_table(decode_string(s2), 'arduino_data', session)



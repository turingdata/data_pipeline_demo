# Generate insert statements for 30 vehicles, linking them to drivers somewhat randomly
#%%
#%%
from faker import Faker
fake = Faker()

vehicle_inserts = ["INSERT INTO vehicles (registration_number, make, model, year, capacity, driver_id) VALUES"]

makes_models = [
    ("Toyota", "Camry"),
    ("Honda", "Civic"),
    ("Ford", "Fiesta"),
    ("Chevrolet", "Malibu"),
    ("Nissan", "Altima"),
    ("Hyundai", "Elantra"),
    ("Volkswagen", "Jetta"),
    ("Subaru", "Impreza"),
    ("Mazda", "3"),
    ("Kia", "Optima")
]

for i in range(1, 31):  # Assuming vehicle_id starts at 1 and increments
    make, model = fake.random_element(elements=makes_models)
    registration_number = fake.bothify(text='??? ####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    year = fake.year()
    capacity = fake.random_int(min=4, max=7)  # Random seating capacity between 4 and 7
    driver_id = fake.random_int(min=1, max=50)  # Assuming there are 50 drivers
    vehicle_inserts.append(f"('{registration_number}', '{make}', '{model}', {year}, {capacity}, {driver_id})")

# Combine all inserts into a single string with comma separation
vehicle_inserts_sql = ",\n".join(vehicle_inserts) + ";"

vehicle_inserts_sql

# %%

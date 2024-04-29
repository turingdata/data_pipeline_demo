#%%
from faker import Faker
fake = Faker()

# Generate insert statements for 50 drivers
driver_inserts = ["INSERT INTO drivers (name, license_number, contact_info, details) VALUES"]

for _ in range(50):
    name = fake.name()
    license_number = fake.bothify(text='D#######')
    job = fake.job()
    id = fake.ssn()
    driver_inserts.append(f"('{name}', '{license_number}', '{job}', '{id}')")

# Combine all inserts into a single string with comma separation
driver_inserts_sql = ",\n".join(driver_inserts) + ";"

driver_inserts_sql

# %%

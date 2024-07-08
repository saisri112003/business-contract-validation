import pandas as pd 
from faker import Faker


classes = {
    0: "Services Provided", 
    1: "Payment", 
    2: "Term", 
    3: "Confidentiality", 
    4: "Termination", 
    5: "Governing Law", 
    6: "Signatures"
}

Faker = Faker()
def generate_contract_text() -> str:
    service_provider_name = Faker.company()
    client_name = Faker.company()
    amount = Faker.random_number(digits=5)
    start_date = Faker.date_this_year()
    end_date = Faker.date_this_year()
    state = Faker.state()
    notice_days = Faker.random_int(min=30, max=90)


    datasets =[
        [f"{service_provider_name} agrees to provide the following services to {client_name}. services are service1 service2, service3.", 0],
        [f"{client_name} agrees to pay {service_provider_name} the amount of ${amount} for the services described above. Payment shall be made within {notice_days} days of receiving an invoice from {service_provider_name}.", 1],
        [f"This contract will commence on {start_date} and will continue until {end_date} unless terminated earlier in accordance with the Termination clause.", 2],
        [f"Both parties agree to maintain the confidentiality of any proprietary or confidential information disclosed during the term of this contract. This obligation will continue beyond the termination of this contract.", 3],
        [f"Either party may terminate this contract with {notice_days} days written notice to the other party. In the event of termination, {service_provider_name} will be compensated for all services performed up to the date of termination.", 4],
        [f"This contract shall be governed by and construed in accordance with the laws of the State of {state}.", 5],
        [f"{service_provider_name}", 6],
        [f"{client_name}", 6]
    ]
    return pd.DataFrame(datasets)

df = generate_contract_text()
df1 = generate_contract_text()
all_df = []
for i in range(10):
    all_df.append(generate_contract_text())
df_concat = pd.concat(all_df)
df_concat.columns = ["features", "label"]
df_concat.to_csv("test.csv", index=False)
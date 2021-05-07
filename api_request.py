import pandas as pd, requests
import psycopg2

# extract data from link using request api
url_pop = 'https://datausa.io/api/data?drilldowns=Nation&measures=Population'
url_pop = requests.get(url_pop)
usr_status = url_pop.status_code
# print(usr_status)

data_api = url_pop.json()
# print(data_api)

# transform
a = []
for i in data_api['data']:
    idn = i['ID Nation']
    nat = i['Nation']
    idy = i['ID Year']
    year = i ['Year']
    pop = i['Population']
    slg = i['Slug Nation']
    cols = [idn, nat, idy, year, pop, slg]
    a.append(cols)

# to dataframe
df = pd.DataFrame(a, columns =['id_nation',
                                'nation',
                                'id_year',
                                'year',
                                'population',
                                'slug_nation'])
# print(df)


# create connection
connection = psycopg2.connect (
    user = "postgres",
    password = "Pml99",
    host = "localhost",
    port = "5432",
    database = "api_request_popus"
)
cursor = connection.cursor()

# create column lists for insertion
cols = ",".join([str(i) for i in df.columns.tolist()])
for i, row in df.iterrows():
    # sql = "INSERT INTO irispipeline (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
    
    sql = "INSERT INTO apipop (" +cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))

    connection.commit()
# print("done!")

def view():
    cursor.execute("""
        select * from apipop
    """)
    data = cursor.fetchall()
    df1 = pd.DataFrame(data, columns = [
        'id',
        'id_nation',
        'nation',
        'id_year',
        'year',
        'population',
        'slug_nation'
    ])

    print(df1)
view()
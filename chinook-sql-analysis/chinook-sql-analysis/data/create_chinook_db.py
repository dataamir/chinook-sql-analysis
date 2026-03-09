"""
Creates a realistic Chinook-style SQLite database with all standard tables:
Artist, Album, Track, Genre, MediaType, Playlist, PlaylistTrack,
Employee, Customer, Invoice, InvoiceLine
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "chinook.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ── Schema ────────────────────────────────────────────────────────────────
    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Genre (
        GenreId   INTEGER PRIMARY KEY,
        Name      TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS MediaType (
        MediaTypeId INTEGER PRIMARY KEY,
        Name        TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Artist (
        ArtistId INTEGER PRIMARY KEY,
        Name     TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Album (
        AlbumId  INTEGER PRIMARY KEY,
        Title    TEXT NOT NULL,
        ArtistId INTEGER NOT NULL,
        FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
    );

    CREATE TABLE IF NOT EXISTS Track (
        TrackId     INTEGER PRIMARY KEY,
        Name        TEXT NOT NULL,
        AlbumId     INTEGER,
        MediaTypeId INTEGER NOT NULL,
        GenreId     INTEGER,
        Composer    TEXT,
        Milliseconds INTEGER NOT NULL,
        Bytes       INTEGER,
        UnitPrice   REAL NOT NULL,
        FOREIGN KEY (AlbumId)     REFERENCES Album(AlbumId),
        FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId),
        FOREIGN KEY (GenreId)     REFERENCES Genre(GenreId)
    );

    CREATE TABLE IF NOT EXISTS Playlist (
        PlaylistId INTEGER PRIMARY KEY,
        Name       TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS PlaylistTrack (
        PlaylistId INTEGER NOT NULL,
        TrackId    INTEGER NOT NULL,
        PRIMARY KEY (PlaylistId, TrackId),
        FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId),
        FOREIGN KEY (TrackId)    REFERENCES Track(TrackId)
    );

    CREATE TABLE IF NOT EXISTS Employee (
        EmployeeId      INTEGER PRIMARY KEY,
        LastName        TEXT NOT NULL,
        FirstName       TEXT NOT NULL,
        Title           TEXT,
        ReportsTo       INTEGER,
        BirthDate       TEXT,
        HireDate        TEXT,
        Address         TEXT,
        City            TEXT,
        State           TEXT,
        Country         TEXT,
        PostalCode      TEXT,
        Phone           TEXT,
        Fax             TEXT,
        Email           TEXT,
        FOREIGN KEY (ReportsTo) REFERENCES Employee(EmployeeId)
    );

    CREATE TABLE IF NOT EXISTS Customer (
        CustomerId   INTEGER PRIMARY KEY,
        FirstName    TEXT NOT NULL,
        LastName     TEXT NOT NULL,
        Company      TEXT,
        Address      TEXT,
        City         TEXT,
        State        TEXT,
        Country      TEXT NOT NULL,
        PostalCode   TEXT,
        Phone        TEXT,
        Fax          TEXT,
        Email        TEXT NOT NULL,
        SupportRepId INTEGER,
        FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)
    );

    CREATE TABLE IF NOT EXISTS Invoice (
        InvoiceId         INTEGER PRIMARY KEY,
        CustomerId        INTEGER NOT NULL,
        InvoiceDate       TEXT NOT NULL,
        BillingAddress    TEXT,
        BillingCity       TEXT,
        BillingState      TEXT,
        BillingCountry    TEXT NOT NULL,
        BillingPostalCode TEXT,
        Total             REAL NOT NULL,
        FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
    );

    CREATE TABLE IF NOT EXISTS InvoiceLine (
        InvoiceLineId INTEGER PRIMARY KEY,
        InvoiceId     INTEGER NOT NULL,
        TrackId       INTEGER NOT NULL,
        UnitPrice     REAL NOT NULL,
        Quantity      INTEGER NOT NULL,
        FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId),
        FOREIGN KEY (TrackId)   REFERENCES Track(TrackId)
    );
    """)

    # ── Seed Data ─────────────────────────────────────────────────────────────
    genres = [
        (1,"Rock"),(2,"Jazz"),(3,"Metal"),(4,"Alternative & Punk"),
        (5,"Rock And Roll"),(6,"Blues"),(7,"Latin"),(8,"Reggae"),
        (9,"Pop"),(10,"Soundtrack"),(11,"Bossa Nova"),(12,"Easy Listening"),
        (13,"Heavy Metal"),(14,"R&B/Soul"),(15,"Electronica/Dance"),
        (16,"World"),(17,"Hip Hop/Rap"),(18,"Science Fiction"),
        (19,"TV Shows"),(20,"Classical"),
    ]
    cur.executemany("INSERT OR IGNORE INTO Genre VALUES (?,?)", genres)

    media_types = [
        (1,"MPEG audio file"),(2,"Protected AAC audio file"),
        (3,"Protected MPEG-4 video file"),(4,"Purchased AAC audio file"),
        (5,"AAC audio file"),
    ]
    cur.executemany("INSERT OR IGNORE INTO MediaType VALUES (?,?)", media_types)

    artists = [
        (1,"AC/DC"),(2,"Accept"),(3,"Aerosmith"),(4,"Alanis Morissette"),
        (5,"Alice In Chains"),(6,"Audioslave"),(7,"BackBeat"),(8,"Billy Cobham"),
        (9,"Black Label Society"),(10,"Black Sabbath"),(11,"Body Count"),
        (12,"Bruce Dickinson"),(13,"Buddy Guy"),(14,"Caetano Veloso"),
        (15,"Chico Buarque"),(16,"Chico Science & Nação Zumbi"),
        (17,"Cidade Negra"),(18,"Cláudio Zoli"),(19,"David Coverdale"),
        (20,"Deep Purple"),(21,"Def Leppard"),(22,"Djavan"),(23,"Ed Motta"),
        (24,"Edo De Waart"),(25,"Elis Regina"),(26,"Eric Clapton"),
        (27,"Faith No More"),(28,"Foo Fighters"),(29,"Frank Sinatra"),
        (30,"Funk Como Le Gusta"),
    ]
    cur.executemany("INSERT OR IGNORE INTO Artist VALUES (?,?)", artists)

    albums = [
        (1,"For Those About To Rock We Salute You",1),
        (2,"Balls to the Wall",2),(3,"Restless and Wild",2),
        (4,"Let There Be Rock",1),(5,"Big Ones",3),
        (6,"Jagged Little Pill",4),(7,"Facelift",5),
        (8,"Superunknown",5),(9,"Audioslave",6),
        (10,"Out of Exile",6),(11,"BackBeat Soundtrack",7),
        (12,"The Best Of Billy Cobham",8),(13,"Alcohol Fueled Brewtality",9),
        (14,"Black Sabbath",10),(15,"Black Sabbath Vol. 4",10),
        (16,"Body Count",11),(17,"Chemical Wedding",12),
        (18,"Blues Deluxe",13),(19,"Prenda Minha",14),
        (20,"Minha Historia",14),(21,"Parabolicamará",16),
        (22,"Acústico MTV",17),(23,"Serie Sem Limite",18),
        (24,"Chill: Brazil",19),(25,"Quanta Gente Veio Ver",25),
        (26,"Unplugged",26),(27,"Angel Dust",27),
        (28,"The Real Thing",27),(29,"In Your Honor",28),
        (30,"One By One",28),
    ]
    cur.executemany("INSERT OR IGNORE INTO Album VALUES (?,?,?)", albums)

    # Generate realistic tracks
    track_names = [
        "For Those About To Rock","Put The Finger On You","Let's Get It Up",
        "Inject The Venom","Snowballed","Evil Walks","C.O.D.","Breaking The Rules",
        "Night Of The Long Knives","Spellbound","Balls to the Wall","Restless and Wild",
        "Fast As a Shark","Princess of the Dawn","Rock You Like a Hurricane",
        "I'm a Rebel","Back Into The Future","Something Like That","Smoke On The Water",
        "Highway Star","Child In Time","Space Truckin'","Black Night","Speed King",
        "Whole Lotta Love","Stairway to Heaven","Kashmir","Rock and Roll","Immigrant Song",
        "Paranoid","Iron Man","War Pigs","Black Sabbath","The Wizard","N.I.B.",
        "Fairies Wear Boots","Sweet Leaf","Into The Void","After Forever","Snowblind",
        "Cornucopia","Laguna Sunrise","St. Vitus Dance","Wheels Of Confusion",
        "Walk On Water","Tomorrow's Dream","Changes","FX","Supernaut","Sabbath Bloody Sabbath",
        "Fluff","National Acrobat","Sabbra Cadabra","Killing Yourself To Live",
    ]

    random.seed(42)
    tracks = []
    for i in range(1, 351):
        album_id = random.randint(1, 30)
        genre_id = random.randint(1, 15)
        media_id = random.choice([1, 1, 1, 2, 4, 5])
        name = random.choice(track_names) + (f" (Part {random.randint(1,3)})" if random.random() > 0.7 else "")
        ms = random.randint(150_000, 400_000)
        price = random.choice([0.99, 0.99, 0.99, 1.29, 1.99])
        tracks.append((i, name, album_id, media_id, genre_id, None, ms, ms * 32, price))
    cur.executemany("INSERT OR IGNORE INTO Track VALUES (?,?,?,?,?,?,?,?,?)", tracks)

    # Playlists
    playlists = [
        (1,"Music"),(2,"Movies"),(3,"TV Shows"),(4,"Audiobooks"),
        (5,"90's Music"),(6,"Audiobooks"),(7,"Movies"),(8,"Music"),
        (9,"Music Videos"),(10,"TV Shows"),(11,"Brazilian Music"),
        (12,"Classical"),(13,"Classical 101 - Deep Cuts"),
        (14,"Classical 101 - Next Steps"),(15,"Classical 101 - The Basics"),
        (16,"Grunge"),(17,"Heavy Metal Classic"),(18,"On-The-Go 1"),
    ]
    cur.executemany("INSERT OR IGNORE INTO Playlist VALUES (?,?)", playlists)

    playlist_tracks = set()
    for _ in range(800):
        pl = random.randint(1, 18)
        tr = random.randint(1, 350)
        playlist_tracks.add((pl, tr))
    cur.executemany("INSERT OR IGNORE INTO PlaylistTrack VALUES (?,?)", list(playlist_tracks))

    # Employees
    employees = [
        (1,"Adams","Andrew","General Manager",None,"1962-02-18","2002-08-14","11120 Jasper Ave NW","Edmonton","AB","Canada","T5K 2N1","+1 (780) 428-9482","+1 (780) 428-3457","andrew@chinookcorp.com"),
        (2,"Edwards","Nancy","Sales Manager",1,"1958-12-08","2002-05-01","825 8 Ave SW","Calgary","AB","Canada","T2P 2T3","+1 (403) 262-3443","+1 (403) 262-3322","nancy@chinookcorp.com"),
        (3,"Peacock","Jane","Sales Support Agent",2,"1973-08-29","2002-04-01","1111 6 Ave SW","Calgary","AB","Canada","T2P 5M5","+1 (403) 262-3443","+1 (403) 262-6712","jane@chinookcorp.com"),
        (4,"Park","Margaret","Sales Support Agent",2,"1947-09-19","2003-05-03","683 10 Street SW","Calgary","AB","Canada","T2P 5G3","+1 (403) 263-4423","+1 (403) 263-4289","margaret@chinookcorp.com"),
        (5,"Johnson","Steve","Sales Support Agent",2,"1965-03-03","2003-10-17","7727B 41 Ave","Calgary","AB","Canada","T3B 1Y7","1 (780) 836-9987","1 (780) 836-9543","steve@chinookcorp.com"),
        (6,"Mitchell","Michael","IT Manager",1,"1973-07-01","2003-10-17","5827 Bowness Road NW","Calgary","AB","Canada","T3B 0C5","+1 (403) 246-9887","+1 (403) 246-9899","michael@chinookcorp.com"),
        (7,"King","Robert","IT Staff",6,"1970-05-29","2004-01-02","590 Columbia Boulevard West","Lethbridge","AB","Canada","T1K 5N8","+1 (403) 456-9986","+1 (403) 456-8485","robert@chinookcorp.com"),
        (8,"Callahan","Laura","IT Staff",6,"1968-01-09","2004-03-04","923 7 ST NW","Lethbridge","AB","Canada","T1H 1Y8","+1 (403) 467-3351","+1 (403) 467-8772","laura@chinookcorp.com"),
    ]
    cur.executemany("INSERT OR IGNORE INTO Employee VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", employees)

    # Customers across many countries
    countries = [
        "USA","USA","USA","USA","USA","USA","Canada","Canada","Brazil","Brazil",
        "Germany","Germany","UK","UK","France","France","Australia","India",
        "Netherlands","Portugal","Norway","Czech Republic","Denmark","Poland",
        "Argentina","Chile","Hungary","Finland","Sweden","Austria",
        "Belgium","Spain","Italy","Singapore","Ireland",
    ]
    cities = [
        "New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia",
        "Toronto","Vancouver","São Paulo","Rio de Janeiro",
        "Berlin","Frankfurt","London","Manchester","Paris","Lyon",
        "Sydney","Mumbai","Amsterdam","Lisbon","Oslo","Prague",
        "Copenhagen","Warsaw","Buenos Aires","Santiago","Budapest",
        "Helsinki","Stockholm","Vienna","Brussels","Madrid","Rome",
        "Singapore","Dublin",
    ]
    first_names = ["Luís","Leonie","François","Helena","Hugh","Victor","Hannah","Astrid",
                   "Mark","Jennifer","Frank","Jack","Michelle","Kathy","Heather","John",
                   "Tim","Dan","Manoj","Puja","Luis","Jorge","Emma","Ellie","Aaron",
                   "Martha","Niklas","Camille","Isabelle","Stanisław","Fynn","Dominique"]
    last_names  = ["Gonçalves","Köhler","Tremblay","Holý","O'Reilly","Stevens","Schneider",
                   "Thorpe","Taylor","Smith","Harris","Wilson","Martin","Thompson","White",
                   "Brown","Jones","Garcia","Davis","Miller","Anderson","Thomas","Jackson",
                   "Lee","Robinson","Clark","Walker","Hall","Allen","Young","Hernandez","King"]

    random.seed(7)
    customers = []
    for i in range(1, 60):
        idx = (i - 1) % len(countries)
        fn  = first_names[i % len(first_names)]
        ln  = last_names[i  % len(last_names)]
        sup = random.choice([3, 4, 5])
        city = cities[idx]
        country = countries[idx]
        customers.append((
            i, fn, ln, None, f"{i} Main St", city, None, country,
            f"{random.randint(10000,99999)}", None, None,
            f"{fn.lower()}.{ln.lower()}{i}@example.com", sup
        ))
    cur.executemany("INSERT OR IGNORE INTO Customer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", customers)

    # Invoices: 2 years of data
    random.seed(99)
    invoice_id = 1
    invoiceline_id = 1
    invoices_data = []
    lines_data = []

    start_date = datetime(2022, 1, 1)
    for _ in range(412):
        cust_id = random.randint(1, 59)
        country = customers[cust_id - 1][7]
        city    = customers[cust_id - 1][5]
        days_offset = random.randint(0, 730)
        inv_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d %H:%M:%S")

        num_lines = random.randint(1, 8)
        total = 0.0
        line_rows = []
        for _ in range(num_lines):
            track_id = random.randint(1, 350)
            price = random.choice([0.99, 1.29, 1.99])
            qty = 1
            total += price * qty
            line_rows.append((invoiceline_id, invoice_id, track_id, price, qty))
            invoiceline_id += 1

        invoices_data.append((invoice_id, cust_id, inv_date, f"{random.randint(1,999)} Street",
                               city, None, country, None, round(total, 2)))
        lines_data.extend(line_rows)
        invoice_id += 1

    cur.executemany("INSERT OR IGNORE INTO Invoice VALUES (?,?,?,?,?,?,?,?,?)", invoices_data)
    cur.executemany("INSERT OR IGNORE INTO InvoiceLine VALUES (?,?,?,?,?)", lines_data)

    conn.commit()
    conn.close()
    print(f"✅ Chinook database created at: {DB_PATH}")
    print(f"   Tracks: 350 | Customers: 59 | Invoices: {len(invoices_data)} | Lines: {len(lines_data)}")

if __name__ == "__main__":
    create_database()

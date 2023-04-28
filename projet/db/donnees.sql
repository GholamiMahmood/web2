-- Fonctionnalité A1
create table declaration (
  no_declaration integer,
  date_declation text,
  date_insp_vispre text,
  nbr_extermin text,
  date_debuttrait date,
  date_fintrait date,
  no_qr text,
  nom_qr varchar(50),
  nom_arround varchar(80),
  coord_x float,
  coord_y float,
  longitude float,
  latitude float
);                        
-- Fonctionnalité D1
create table tab_extermination (
  id integer primary key,
  quartier varchar(50),
  arrondissement varchar(80),
  adresse varchar(200),
  date date,
  nom_prenom varchar(50),
  description varchar(200) 
);

-- Fonctionnalité E1
create table profile (
  id integer primary key,
  nom varchar(25),
  courriel varchar(90),
  salt varchar(32),
  hash varchar (128),
  photo_id varchar(32) 
);

create table quartiers (
  id integer primary key,
  profile_id integer NOT NULL,
  nom_quartier varchar(50),  
  FOREIGN KEY (profile_id) REFERENCES profile(id) ON DELETE CASCADE
);

create table photos(
  id varchar(32)primary key,
  data blob
);

PGDMP  &                     }            movies    17.0    17.0 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    24580    movies    DATABASE     y   CREATE DATABASE movies WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_India.1252';
    DROP DATABASE movies;
                     postgres    false            �            1259    41155 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap r       postgres    false            �            1259    41154    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public               postgres    false    227            �           0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
          public               postgres    false    226            �            1259    41164    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap r       postgres    false            �            1259    41163    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public               postgres    false    229            �           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
          public               postgres    false    228            �            1259    41148    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap r       postgres    false            �            1259    41147    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public               postgres    false    225            �           0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
          public               postgres    false    224            �            1259    41171 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap r       postgres    false            �            1259    41180    auth_user_groups    TABLE     ~   CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap r       postgres    false            �            1259    41179    auth_user_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.auth_user_groups_id_seq;
       public               postgres    false    233            �           0    0    auth_user_groups_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;
          public               postgres    false    232            �            1259    41170    auth_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auth_user_id_seq;
       public               postgres    false    231            �           0    0    auth_user_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;
          public               postgres    false    230            �            1259    41187    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap r       postgres    false            �            1259    41186 !   auth_user_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.auth_user_user_permissions_id_seq;
       public               postgres    false    235            �           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;
          public               postgres    false    234            �            1259    24598    casts    TABLE     �   CREATE TABLE public.casts (
    actor_id integer NOT NULL,
    actor character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    debut_movie text NOT NULL,
    debut_year integer NOT NULL,
    img character varying(255)
);
    DROP TABLE public.casts;
       public         heap r       postgres    false            �            1259    24597    casts_actor_id_seq    SEQUENCE     �   CREATE SEQUENCE public.casts_actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.casts_actor_id_seq;
       public               postgres    false    218            �           0    0    casts_actor_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.casts_actor_id_seq OWNED BY public.casts.actor_id;
          public               postgres    false    217            �            1259    41246    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap r       postgres    false            �            1259    41245    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public               postgres    false    237            �           0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
          public               postgres    false    236            �            1259    41139    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap r       postgres    false            �            1259    41138    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public               postgres    false    223            �           0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
          public               postgres    false    222            �            1259    41130    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap r       postgres    false            �            1259    41129    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public               postgres    false    221            �           0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
          public               postgres    false    220            �            1259    41282    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap r       postgres    false            �            1259    32772    movie    TABLE     �   CREATE TABLE public.movie (
    id integer DEFAULT floor(((random() * (100000)::double precision) + (1)::double precision)) NOT NULL,
    year integer NOT NULL,
    movie_name character varying(255) NOT NULL,
    genre character varying(100) NOT NULL
);
    DROP TABLE public.movie;
       public         heap r       postgres    false            �            1259    49514    movie_actees    TABLE     �   CREATE TABLE public.movie_actees (
    actress_id integer NOT NULL,
    actress character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    debut_movie text NOT NULL,
    debut_year integer NOT NULL,
    img character varying(100) NOT NULL
);
     DROP TABLE public.movie_actees;
       public         heap r       postgres    false            �            1259    49513    movie_actees_actress_id_seq    SEQUENCE     �   ALTER TABLE public.movie_actees ALTER COLUMN actress_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_actees_actress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    242            �            1259    49530    movie_comedian    TABLE       CREATE TABLE public.movie_comedian (
    comedian_id integer NOT NULL,
    comedian character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    debut_movie text NOT NULL,
    debut_year integer NOT NULL,
    img character varying(100) NOT NULL
);
 "   DROP TABLE public.movie_comedian;
       public         heap r       postgres    false            �            1259    49529    movie_comedian_comedian_id_seq    SEQUENCE     �   ALTER TABLE public.movie_comedian ALTER COLUMN comedian_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_comedian_comedian_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    246            �            1259    49522    movie_direct    TABLE     �   CREATE TABLE public.movie_direct (
    director_id integer NOT NULL,
    director character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    debut_movie text NOT NULL,
    debut_year integer NOT NULL,
    img character varying(100) NOT NULL
);
     DROP TABLE public.movie_direct;
       public         heap r       postgres    false            �            1259    49521    movie_direct_director_id_seq    SEQUENCE     �   ALTER TABLE public.movie_direct ALTER COLUMN director_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_direct_director_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    244            �            1259    65937    movie_genre    TABLE     �   CREATE TABLE public.movie_genre (
    genre_id integer NOT NULL,
    genre character varying(255) NOT NULL,
    img character varying(100) NOT NULL
);
    DROP TABLE public.movie_genre;
       public         heap r       postgres    false            �            1259    65936    movie_genre_genre_id_seq    SEQUENCE     �   ALTER TABLE public.movie_genre ALTER COLUMN genre_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_genre_genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    254            �            1259    49538    movie_music    TABLE     �   CREATE TABLE public.movie_music (
    music_id integer NOT NULL,
    music character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    debut_movie text NOT NULL,
    debut_year integer NOT NULL,
    img character varying(100) NOT NULL
);
    DROP TABLE public.movie_music;
       public         heap r       postgres    false            �            1259    49537    movie_music_music_id_seq    SEQUENCE     �   ALTER TABLE public.movie_music ALTER COLUMN music_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_music_music_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    248            �            1259    49552    movie_review    TABLE     �   CREATE TABLE public.movie_review (
    rating integer NOT NULL,
    review_text text,
    created_at timestamp with time zone NOT NULL,
    movie_id bigint NOT NULL,
    id integer NOT NULL
);
     DROP TABLE public.movie_review;
       public         heap r       postgres    false            �            1259    57750    movie_review_id_seq    SEQUENCE     �   ALTER TABLE public.movie_review ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.movie_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    251            �            1259    49546 	   movie_sho    TABLE     �   CREATE TABLE public.movie_sho (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    img character varying(100) NOT NULL,
    rate double precision NOT NULL,
    year_f integer NOT NULL,
    ep integer NOT NULL
);
    DROP TABLE public.movie_sho;
       public         heap r       postgres    false            �            1259    49545    movie_sho_id_seq    SEQUENCE     �   ALTER TABLE public.movie_sho ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_sho_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    250            �            1259    41276    movie_title    TABLE     x  CREATE TABLE public.movie_title (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    img character varying(100) NOT NULL,
    rate double precision NOT NULL,
    year integer NOT NULL,
    description text,
    release_date date,
    tagline character varying(255),
    watch_trailer character varying(500),
    director_id integer,
    actor_id integer
);
    DROP TABLE public.movie_title;
       public         heap r       postgres    false                        1259    65983    movie_title_genres    TABLE     �   CREATE TABLE public.movie_title_genres (
    id bigint NOT NULL,
    title_id bigint NOT NULL,
    genre_id integer NOT NULL
);
 &   DROP TABLE public.movie_title_genres;
       public         heap r       postgres    false            �            1259    65982    movie_title_genres_id_seq    SEQUENCE     �   ALTER TABLE public.movie_title_genres ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.movie_title_genres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public               postgres    false    256            �            1259    41275    movie_title_id_seq    SEQUENCE     {   CREATE SEQUENCE public.movie_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.movie_title_id_seq;
       public               postgres    false    239            �           0    0    movie_title_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.movie_title_id_seq OWNED BY public.movie_title.id;
          public               postgres    false    238            �           2604    41158    auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    227    226    227            �           2604    41167    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    228    229    229            �           2604    41151    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    225    225            �           2604    41174    auth_user id    DEFAULT     l   ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);
 ;   ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    230    231    231            �           2604    41183    auth_user_groups id    DEFAULT     z   ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);
 B   ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    232    233    233            �           2604    41190    auth_user_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);
 L   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    235    234    235            �           2604    24601    casts actor_id    DEFAULT     p   ALTER TABLE ONLY public.casts ALTER COLUMN actor_id SET DEFAULT nextval('public.casts_actor_id_seq'::regclass);
 =   ALTER TABLE public.casts ALTER COLUMN actor_id DROP DEFAULT;
       public               postgres    false    218    217    218            �           2604    41249    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    236    237    237            �           2604    41142    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    222    223    223            �           2604    41133    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    221    220    221            �           2604    41279    movie_title id    DEFAULT     p   ALTER TABLE ONLY public.movie_title ALTER COLUMN id SET DEFAULT nextval('public.movie_title_id_seq'::regclass);
 =   ALTER TABLE public.movie_title ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    239    238    239            �          0    41155 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public               postgres    false    227   ��       �          0    41164    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public               postgres    false    229   ��       �          0    41148    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public               postgres    false    225   ��       �          0    41171 	   auth_user 
   TABLE DATA           �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public               postgres    false    231   ^�       �          0    41180    auth_user_groups 
   TABLE DATA           A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public               postgres    false    233   '�       �          0    41187    auth_user_user_permissions 
   TABLE DATA           P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public               postgres    false    235   D�       |          0    24598    casts 
   TABLE DATA           ]   COPY public.casts (actor_id, actor, date_of_birth, debut_movie, debut_year, img) FROM stdin;
    public               postgres    false    218   a�       �          0    41246    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public               postgres    false    237   ��       �          0    41139    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public               postgres    false    223   k�                 0    41130    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public               postgres    false    221   "�       �          0    41282    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public               postgres    false    240   S�       }          0    32772    movie 
   TABLE DATA           <   COPY public.movie (id, year, movie_name, genre) FROM stdin;
    public               postgres    false    219   ��       �          0    49514    movie_actees 
   TABLE DATA           h   COPY public.movie_actees (actress_id, actress, date_of_birth, debut_movie, debut_year, img) FROM stdin;
    public               postgres    false    242   
�       �          0    49530    movie_comedian 
   TABLE DATA           l   COPY public.movie_comedian (comedian_id, comedian, date_of_birth, debut_movie, debut_year, img) FROM stdin;
    public               postgres    false    246   ��       �          0    49522    movie_direct 
   TABLE DATA           j   COPY public.movie_direct (director_id, director, date_of_birth, debut_movie, debut_year, img) FROM stdin;
    public               postgres    false    244   ,�       �          0    65937    movie_genre 
   TABLE DATA           ;   COPY public.movie_genre (genre_id, genre, img) FROM stdin;
    public               postgres    false    254   ��       �          0    49538    movie_music 
   TABLE DATA           c   COPY public.movie_music (music_id, music, date_of_birth, debut_movie, debut_year, img) FROM stdin;
    public               postgres    false    248   ��       �          0    49552    movie_review 
   TABLE DATA           U   COPY public.movie_review (rating, review_text, created_at, movie_id, id) FROM stdin;
    public               postgres    false    251          �          0    49546 	   movie_sho 
   TABLE DATA           D   COPY public.movie_sho (id, name, img, rate, year_f, ep) FROM stdin;
    public               postgres    false    250   �      �          0    41276    movie_title 
   TABLE DATA           �   COPY public.movie_title (id, name, img, rate, year, description, release_date, tagline, watch_trailer, director_id, actor_id) FROM stdin;
    public               postgres    false    239   �      �          0    65983    movie_title_genres 
   TABLE DATA           D   COPY public.movie_title_genres (id, title_id, genre_id) FROM stdin;
    public               postgres    false    256   �      �           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public               postgres    false    226            �           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public               postgres    false    228            �           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 68, true);
          public               postgres    false    224            �           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
          public               postgres    false    232            �           0    0    auth_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);
          public               postgres    false    230            �           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
          public               postgres    false    234            �           0    0    casts_actor_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.casts_actor_id_seq', 37, true);
          public               postgres    false    217            �           0    0    django_admin_log_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 116, true);
          public               postgres    false    236            �           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 17, true);
          public               postgres    false    222            �           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 37, true);
          public               postgres    false    220            �           0    0    movie_actees_actress_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.movie_actees_actress_id_seq', 1, true);
          public               postgres    false    241            �           0    0    movie_comedian_comedian_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.movie_comedian_comedian_id_seq', 16, true);
          public               postgres    false    245            �           0    0    movie_direct_director_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.movie_direct_director_id_seq', 40, true);
          public               postgres    false    243            �           0    0    movie_genre_genre_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.movie_genre_genre_id_seq', 10, true);
          public               postgres    false    253            �           0    0    movie_music_music_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.movie_music_music_id_seq', 12, true);
          public               postgres    false    247            �           0    0    movie_review_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.movie_review_id_seq', 11, true);
          public               postgres    false    252            �           0    0    movie_sho_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.movie_sho_id_seq', 10, true);
          public               postgres    false    249            �           0    0    movie_title_genres_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.movie_title_genres_id_seq', 87, true);
          public               postgres    false    255            �           0    0    movie_title_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.movie_title_id_seq', 51, true);
          public               postgres    false    238            �           2606    41273    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public                 postgres    false    227            �           2606    41203 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public                 postgres    false    229    229            �           2606    41169 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public                 postgres    false    229            �           2606    41160    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public                 postgres    false    227            �           2606    41194 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public                 postgres    false    225    225            �           2606    41153 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public                 postgres    false    225            �           2606    41185 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public                 postgres    false    233            �           2606    41218 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public                 postgres    false    233    233            �           2606    41176    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public                 postgres    false    231            �           2606    41192 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public                 postgres    false    235            �           2606    41232 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public                 postgres    false    235    235            �           2606    41268     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public                 postgres    false    231            �           2606    24605    casts casts_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_pkey PRIMARY KEY (actor_id);
 :   ALTER TABLE ONLY public.casts DROP CONSTRAINT casts_pkey;
       public                 postgres    false    218            �           2606    41254 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public                 postgres    false    237            �           2606    41146 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public                 postgres    false    223    223            �           2606    41144 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public                 postgres    false    223            �           2606    41137 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public                 postgres    false    221            �           2606    41288 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public                 postgres    false    240            �           2606    49520    movie_actees movie_actees_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.movie_actees
    ADD CONSTRAINT movie_actees_pkey PRIMARY KEY (actress_id);
 H   ALTER TABLE ONLY public.movie_actees DROP CONSTRAINT movie_actees_pkey;
       public                 postgres    false    242            �           2606    49536 "   movie_comedian movie_comedian_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.movie_comedian
    ADD CONSTRAINT movie_comedian_pkey PRIMARY KEY (comedian_id);
 L   ALTER TABLE ONLY public.movie_comedian DROP CONSTRAINT movie_comedian_pkey;
       public                 postgres    false    246            �           2606    49528    movie_direct movie_direct_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.movie_direct
    ADD CONSTRAINT movie_direct_pkey PRIMARY KEY (director_id);
 H   ALTER TABLE ONLY public.movie_direct DROP CONSTRAINT movie_direct_pkey;
       public                 postgres    false    244            �           2606    65941    movie_genre movie_genre_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.movie_genre
    ADD CONSTRAINT movie_genre_pkey PRIMARY KEY (genre_id);
 F   ALTER TABLE ONLY public.movie_genre DROP CONSTRAINT movie_genre_pkey;
       public                 postgres    false    254            �           2606    49544    movie_music movie_music_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.movie_music
    ADD CONSTRAINT movie_music_pkey PRIMARY KEY (music_id);
 F   ALTER TABLE ONLY public.movie_music DROP CONSTRAINT movie_music_pkey;
       public                 postgres    false    248            �           2606    32777    movie movie_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.movie DROP CONSTRAINT movie_pkey;
       public                 postgres    false    219            �           2606    57758    movie_review movie_review_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.movie_review
    ADD CONSTRAINT movie_review_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.movie_review DROP CONSTRAINT movie_review_pkey;
       public                 postgres    false    251            �           2606    49550    movie_sho movie_sho_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.movie_sho
    ADD CONSTRAINT movie_sho_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.movie_sho DROP CONSTRAINT movie_sho_pkey;
       public                 postgres    false    250            �           2606    65987 *   movie_title_genres movie_title_genres_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.movie_title_genres
    ADD CONSTRAINT movie_title_genres_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.movie_title_genres DROP CONSTRAINT movie_title_genres_pkey;
       public                 postgres    false    256            �           2606    65989 E   movie_title_genres movie_title_genres_title_id_genre_id_bf945c7f_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.movie_title_genres
    ADD CONSTRAINT movie_title_genres_title_id_genre_id_bf945c7f_uniq UNIQUE (title_id, genre_id);
 o   ALTER TABLE ONLY public.movie_title_genres DROP CONSTRAINT movie_title_genres_title_id_genre_id_bf945c7f_uniq;
       public                 postgres    false    256    256            �           2606    41281    movie_title movie_title_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.movie_title
    ADD CONSTRAINT movie_title_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.movie_title DROP CONSTRAINT movie_title_pkey;
       public                 postgres    false    239            �           1259    41274    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public                 postgres    false    227            �           1259    41214 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public                 postgres    false    229            �           1259    41215 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public                 postgres    false    229            �           1259    41200 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public                 postgres    false    225            �           1259    41230 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public                 postgres    false    233            �           1259    41229 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public                 postgres    false    233            �           1259    41244 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public                 postgres    false    235            �           1259    41243 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public                 postgres    false    235            �           1259    41269     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public                 postgres    false    231            �           1259    41265 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public                 postgres    false    237            �           1259    41266 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public                 postgres    false    237            �           1259    41290 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public                 postgres    false    240            �           1259    41289 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public                 postgres    false    240            �           1259    49564    movie_review_movie_id_43bc85b0    INDEX     [   CREATE INDEX movie_review_movie_id_43bc85b0 ON public.movie_review USING btree (movie_id);
 2   DROP INDEX public.movie_review_movie_id_43bc85b0;
       public                 postgres    false    251            �           1259    49622    movie_title_actor_id_0a13702d    INDEX     Y   CREATE INDEX movie_title_actor_id_0a13702d ON public.movie_title USING btree (actor_id);
 1   DROP INDEX public.movie_title_actor_id_0a13702d;
       public                 postgres    false    239            �           1259    49596     movie_title_director_id_0c403fa1    INDEX     _   CREATE INDEX movie_title_director_id_0c403fa1 ON public.movie_title USING btree (director_id);
 4   DROP INDEX public.movie_title_director_id_0c403fa1;
       public                 postgres    false    239            �           1259    66001 $   movie_title_genres_genre_id_a17d59ba    INDEX     g   CREATE INDEX movie_title_genres_genre_id_a17d59ba ON public.movie_title_genres USING btree (genre_id);
 8   DROP INDEX public.movie_title_genres_genre_id_a17d59ba;
       public                 postgres    false    256            �           1259    66000 $   movie_title_genres_title_id_0d800210    INDEX     g   CREATE INDEX movie_title_genres_title_id_0d800210 ON public.movie_title_genres USING btree (title_id);
 8   DROP INDEX public.movie_title_genres_title_id_0d800210;
       public                 postgres    false    256            �           2606    41209 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public               postgres    false    4766    229    225            �           2606    41204 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public               postgres    false    4771    229    227            �           2606    41195 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public               postgres    false    4761    223    225            �           2606    41224 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public               postgres    false    233    4771    227            �           2606    41219 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public               postgres    false    4779    231    233            �           2606    41238 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public               postgres    false    225    4766    235            �           2606    41233 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public               postgres    false    231    235    4779            �           2606    41255 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public               postgres    false    4761    223    237            �           2606    41260 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public               postgres    false    4779    237    231            �           2606    49559 =   movie_review movie_review_movie_id_43bc85b0_fk_movie_title_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_review
    ADD CONSTRAINT movie_review_movie_id_43bc85b0_fk_movie_title_id FOREIGN KEY (movie_id) REFERENCES public.movie_title(id) DEFERRABLE INITIALLY DEFERRED;
 g   ALTER TABLE ONLY public.movie_review DROP CONSTRAINT movie_review_movie_id_43bc85b0_fk_movie_title_id;
       public               postgres    false    239    4802    251            �           2606    49617 ;   movie_title movie_title_actor_id_0a13702d_fk_casts_actor_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_title
    ADD CONSTRAINT movie_title_actor_id_0a13702d_fk_casts_actor_id FOREIGN KEY (actor_id) REFERENCES public.casts(actor_id) DEFERRABLE INITIALLY DEFERRED;
 e   ALTER TABLE ONLY public.movie_title DROP CONSTRAINT movie_title_actor_id_0a13702d_fk_casts_actor_id;
       public               postgres    false    218    239    4753            �           2606    49597 H   movie_title movie_title_director_id_0c403fa1_fk_movie_direct_director_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_title
    ADD CONSTRAINT movie_title_director_id_0c403fa1_fk_movie_direct_director_id FOREIGN KEY (director_id) REFERENCES public.movie_direct(director_id) DEFERRABLE INITIALLY DEFERRED;
 r   ALTER TABLE ONLY public.movie_title DROP CONSTRAINT movie_title_director_id_0c403fa1_fk_movie_direct_director_id;
       public               postgres    false    239    4810    244            �           2606    65995 O   movie_title_genres movie_title_genres_genre_id_a17d59ba_fk_movie_genre_genre_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_title_genres
    ADD CONSTRAINT movie_title_genres_genre_id_a17d59ba_fk_movie_genre_genre_id FOREIGN KEY (genre_id) REFERENCES public.movie_genre(genre_id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.movie_title_genres DROP CONSTRAINT movie_title_genres_genre_id_a17d59ba_fk_movie_genre_genre_id;
       public               postgres    false    254    4821    256            �           2606    65990 I   movie_title_genres movie_title_genres_title_id_0d800210_fk_movie_title_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.movie_title_genres
    ADD CONSTRAINT movie_title_genres_title_id_0d800210_fk_movie_title_id FOREIGN KEY (title_id) REFERENCES public.movie_title(id) DEFERRABLE INITIALLY DEFERRED;
 s   ALTER TABLE ONLY public.movie_title_genres DROP CONSTRAINT movie_title_genres_title_id_0d800210_fk_movie_title_id;
       public               postgres    false    4802    256    239            �      x������ � �      �      x������ � �      �   �  x�m�[��0E��Ud��W���FK#D�4R����]t�\�c��܂�����z=,�r�!�u�ֱ�^���,m,�(���{^����
��}�'���n-����!��
0Xk(cc%,E"����G��*Y����3O�~��q%��FLGk�Hҳp��&Ej�Pд`)��i|=C�����~�'5Bjk�	Ҩ�A���<��eLg{?u�z.�v�r ���Mm��In��aY����̡��vb᲼�I��.�;��or��Aױ��9��za�b�2�y
���	f�X	�i��y��ඎ��8���!��?&DL��'�mMq�-��.�@U,]��!�\�#�L�AN�(�9��NFk��N���!J}6�::bXM���r���oj�b���0�R��0e���0Q��{�k�!4tXǪ�����'?kJʠ1y�S��S���k�E�]� )b\��!bL�� �k���1$|-��X�(S�g{�S��z��R�y�ij��톄�c�b�R�]ϔK�R$ATcR��0��]?�����73�q���Nȸ�
ß'dL^����5��q��?"�����^�@�c���� ���Y���g9L�Κ��?�!۟���1���A�      �   �   x�%��
�@E��S�p�|�8�4T�����	b�23�P�|����Ņ�����E#wM)h�Y�֏`�~�O�nR'#��Yj�\��N��_�B�+N?�#���ދ��\٧L��s�'H�[,`p�ʑ��^�r�(��UW�����u+*i����E{׿�cZ�;�JE�����`����4A      �      x������ � �      �      x������ � �      |   d  x�M��n�0�����sB��鎪���%��i:-1$N�����0!EB���}qI'!�d_w0���!�m� 48�<B�wQ@Z��}��K�&��8�	?���K]�2��撵*j�k��%��ƫ�gi�7���j���i����"<��/��K���2d�_��)ى\L[�a��y$$��,
�껾�䅿�\@r��q%l�xS�J�Ϛ�a"���썏LH�%H�����dS��ʆ&�"��ص�|��mn7�H.�A��8�q�[��Y��t�d����g���8�5�j�0��I�4��C�j���n�.3�������]ck�����5�Ft@�f������=f`�g3�vj��%PW�YO��м�-�h�(�L8n���.
���$��fuvg�>�,��N��'=��9k��C��J܍�__��	��v�L ���~x4`,P~��[����4~\_~�Q"-�pKWdb���J+tm+*�����h�to�o��c��i+$�����
S+F��1a�A�?�AP���~��!MvI��?���l)��u��Es�j�1�8XW|4�@������������֚?���x'�      �   �  x���Mo������ �룿xs H����v�0+͊L(ɠ�����T5�d�4E��`��{z�z���@���=����%a�|`���K2X�ֻM������j��~/���/��u}�l~����_�NQֵ�?�P���"��$ߢ%#��j,��d_�{����k,�Y�Dׂc2㾬b��)�%P�dm>{�X���S��F6���+����F�k�]���u���n��������A�����n�_�0��%B� m|�������ض���f���*4,.�[��b0Z��;Ѓk ,-.�[�3��E�9��4�$�Zd��%�wG����7 R�ږ"�qs���a�Ph���v��Ј�$Z`����??i��� ��.�(bB����2����0�'8!��]�����g.h\\�k#�K������m����#V�G��T�X2 ��Du 	E����x\j=9��'��8M��Z�(59�z(�X���u�/�T���t�+�\�ou�-�o�M�x.��rƑ����9\�?`	��8v�z(����<�)�=��N=
�|�s������y��S���͓<�p��hRo��% 
X
��cIo�Z<3�z��Q�ET���Z XB\��Y�Z XB�G��V����[��B�(�|5>�
��
�x��k�`Q�j����Œ�l��>�-,��(*k��B8h��AW�4�h�xo�Ϻ��1`i)��f��I��e�����R&M�C��n���������{)��l�m0�X(/�S��u/E[��Z+�R����Yo^
vS0Ɩ1 ������n�m�u�/]�OW`��^�˸y����)7q�vG"Û�XR��n�\��o�3G�X�Ԁ+�<{��߻��T\k
��Ԇ0��yM�J��<�DgA�b �gS|�.Z4;�8T��GD�֏%�t	�١l���%B��I�e"]�iv0p�q�[�X��C��ty�Ql©�?7]��d�˵g�}����+I
�����;��:�T�Q��#���F+/��ؠ��y�.(��`����=������W��Z5�� �"@g�riƗY��l��rO��Ek؊�)���^�*>��K5�-�L�|���4�9����5���z1N]�{���U�[ͷK�Z#��t�!���n�h�c��8��8�7 �����F:����_�Lop�Z�$��=��<4����� Ԫ��-��r�;�eu��ՙV��{�5I·�q!K�'�����Z��R�����bF/כ���c��c�w��'�"�(/�E�|0D���#xZ�,�ܷ>�P����?ݙF��浆��b2��~�Mv?+; �h�ӥ���^f*^|zܬ_�w�_�b�Z�=����}�x j��`$�"Q)�v��}�}������'�N��ep���a� �w�0j��Hh�4j�'s�.|�17z�����J�������Vj�3��ci�
X���x�g����hR�^i 3Y�M
ּ��Ye�r˖�#O^ּ�����& �be5�.��/}���:)E��o��+x�t�-˟8�w��{8�PMҐN�a�@a�h���y��\O�h4������Q�����ϯ��b!]YƘ�/^|�����笥���Ϙ"�P>�}��ޠNF-�4�S�M�����k>w��h��K�=ٱ�?=k�?g�Z{(Z/l����r�V_�e�e�7�7��W�
M#
��ɴ�?f�"-��m���Iڟ��M�e}��嵞)�i�3���|�ya��Z��(%�=��)�������M��:�C����[����{���+��R�̉`�g/%��7YM���ʤ>�G�u��F`t��$Gق̢.���x�ϥK�����e�yx/�T#�7��t��ʻ�W�e�[=~�v�7ت.֧6M���@�����Wi0�Bؘ�"o�LS��3�����#�KCLX�-*�������b���q1���P~4s�����8�q�~����n��80S\��L�`}n�Ǹy��ǁ�!�)ׁ����cܼ���P�H^��
�ݦ���7���8R�TVc����+ܼ���x��7�$�b�Ǹyo���)�ew�ȥ����w�y2�2�D�՘�y<�����ݻw��9a�      �   �   x�M�K�0Dי� �w6Qj�%�T���	%lF~c�,�\�Oagb���1Jr�|�de���jw7q��*9a�:�����r�х���l�X�'���u-p�{�WS\:�`���?��1u�p0�n��ȣ��w'V� :�=�
7}���ۑ�A�5���KCq� x�H`O         !  x����n�0��O��C�u��DK���N���hז�4]���|"e��v��8~��B���j�B�C�����䏰	�$�TJ�p���TY$w��T�*2Y��
}ݝ�������ޣ�*:���MJ�C#3��>ƪk��:��᭫��]�a�Zp��{�ִ��_|�x�fQ�řd'�P�����7�0L�M߄������.M����l�Ʌv�+6����e�R[��5՝��VY$�B�0���a�IT�⥾��1' �4���R���y~2��fv��k���C]�������]�8��M,G;e"ڻN=pݙ��@%����S4��=�J��N}w9?Gr���H�/g�+�s���؄��W�� n�Jaܶ����q�����U�ѭ�2���n7ĥ��J��E>pm`��:�����=�#x;-�]����x���E�D����8L�-f��n����2�["�
9�Dn]=�7�oUJM�q��R�*��y�㕊����B�֜!e��l�
�L�R����D�u�7��:d���p*�3䈒&��޺+��ǆ�P�B:g����C_������l�N��|ń�蛮��qz��=���(���\:�������V�J�Q�I�Ŝ(ެm��r2�T�-����S�k��_��$=R8-�Y�9[ ?[N"�{P%��N�n���������m��`��/�)�Wq�T�Æ�C��|�Zq�����馓�tʤ̙���Y+���v6"G��g���j�_��V�"J��Qk9?�����U��      �   �  x���Ɏ�@  �s�W�}�)�
(�!*� n�M&!������O:���A���~�(�􁄮��	 �E�����yd�t���T����9ק�	����m�@_�8����l��A�.�b1�9��qY9�Dlg���M7+�"�!9s_v�h#���n���E�l�g�W���k����(�)y��
d�E��\+}s5���������"I�L�{����2�,���[z�=g�x]݇�����u}�[IR\����b6	
~� �3�� ���%ùH0�_��xg�<HɃ�8�$� �i^f-��_f@?s�Z��i����V�|o��	��I�8�%EIk�v������C8~/Q�p�Α�����3��>���
�f���V_KT9({O����vs���������_{���!8Zg�;��>>�<fly�֝�����Eʥ]E��ktEL�|�:(�e|�_//�A��ssT��Xj�^�*Ou�Qmu�/�z��P[X���`���h�|%ݔ֐��px\�YJ �^N�j��?9��[�x�]Y�������99��I]��W�"�|�W8GE��e�h�qL��OLҞ������(Vf���N؝l��	F���\xF�\�4��7��2��D�C�������?�vyh      }     x�m�MN�0�}
 �x�ɲ$B)��(��P�F�i��c7U+Q��O���@eRH�b�k�B+�=��a"��H����Q��>�[&��h{���)�<�޽s4����]Ӟi}OZ��VfI���?L2r��3ZDǶ�m(t#3ס�tG�^���Bί�S���ı���ɢ(WO"��-ZV�]�$��wM=siT7$+�;htt}�YsH����NcK���D{jB��X�"[Bv4q��N}�(mVQ�Q�G��	��a����_�D      �   �  x�M��n�0��'O����p�"�h�U���i�b
��@+�~=&j{k�|眙�P誗<���r�5$ݨ�eǲ�&��<���V��?E�;���F�f�>n�w!�	� Q[�����$���+�u��B�3$'�Z��S7Ȫ&�8�%�bS��0�������Z���dG��r$G��{�J����e��'y�t���D��NX��ԃ�X>겗��Ys���V)�Q-1�3#�n�bw��5��F��r&�����C>�JM}�:�>����AA"���=���(Q]Xn�uf��K3�DA�g����ǆ�s
�m ��Wc�8̊ �Y�j3�+���llh�K��C��O�����(�I�e"��b�������w�v܍�C8`�˶b16����;'{q��Ez�b����铒������8tu]c�v������<��d      �   G  x�M�ao�0�?�_�?�ݶ����"�$Knb��@'c7ۯ���-KL���=�y�SA4��Z�.9�IARho`���|N�����V�j�2�>��U3IJ8��K3`��B&$Y�t�U�@�	����Q�T��\?\�G6�О�6��B�}&}"��Ox�Mk��c�&?d+��,v�s�/-�j��/���H��+�@��zu��d~����+�I�Ưַ`?��׶l�𛖗�<8"S��'�zAt���9c|�d@�6���Lh2|ՃN��M乫��d�-}�&�;�u�9���HE#�� ����Y���ƥm�B�-{��5���
'��V�Q|,�W��NGp�@?�p�ֹS$s���b�LTqȔK�"t'�b�z�0NL�,�O���*�Sc�'�ԣ�%I5�j�c&V!pk��D�n�8��iW�_�S}��J��QjN���Jc����� �oK�v;��$�K�*~��d�1W(�j��.=�$櫆�!��q+L;�Åߠ�n�X ��r�!x�ƅ��gh0������@���2�Hѝ:��H���*�x��J�ŔE�(���7�����?14      �   n  x��V]��H|���t�G�p4 ��d�3r����뷺n��M1��t�s��['>+9ٽdї3s��g�=�s���*[����ń��g�o��r;�$�Xye5>�����s�I�{����e9V�Y���k�+�5�)}P?-+�z��Ș��%�Sbh��l����cz�y�X-7��F�r�Mɾ�S�x���
;ڇ����
d�x��g�J���).���6�K��������8�╌4ɶ��MF=V�si��)�ؽ-Dx��v�ّ#��$J���@���PM �zUyJ��޷��-��8�Ry��Ll;��M���]��ޫ�%9d\e%��������&�D�%��w�>8�F�ѱ�H����9��cHU��}��'����@X�m�a��ݬ4	��;�h&Rղ�ګc��Bc�縀�S��'Zv��Kt]+�F�y/g4bW�<m�R���~d�I�g�\�D��j�x��$>�p���[yn~���'�@ϕ�Ļ��g6�sok����4��YQ�9W���0����wTc}�[�.�*M�3G~.W��+�-�J�|_��x)st7��1����/��޳VL����V�V�׈��#�k�v���ـ��Is9��w��t����EQZ�A���ϴnE��d����m��,��/���e|+�� !���WA�.�=!ny�[�/�d�J=�vt4>��E����B6!GV4`���������h�1'~����#�M���?��*Ŕ�>ҜӀz5o��)�k�z�󼅧� I)@���ݺ�w�����T2S0��igSId�V4�\:Qc�#�XԐ�����d�y�_?TJTQ�E)���K�[4L�[C���Ϟ�nmv��u��n�遢�������B�����Dn�s�V��+Ë�D3b��o��,:Ѩ��f@����]X��+ɜ���r�2,IDct��,N3�g�)�W�'�Tb�����J���� �b�?�4�(��uAe�3J��m!� M?���Ϊ�q(
���`����.#��.2� 3L�a���b)�,x+��rpf@�H"J����#��
cy���$��1SW�'c�Niz�!h�:�%�g䳂���zC
��m���|�k�����fL�Ҹ;Li>d�A^2�#�m�B���a�_���J7'A�7UI�<緡r����r��Iu������F� �<{;O� �.���)J��^�2��pjj��n��P�ʉ��SeZ<W�@��G��.[�Sұ#O�1%Ý>��j��2�eU٤��=��^\�0� ��i������|������&YY�����zVXAGj�����#���k]�(��᭩�2��㗗��s�M      �   �   x�-�]O�0���)���9	�q�"s&'M�P�-�݆��Ɩ�����䜃ћDR�fN͝��K9�7�s$�}�|���NC5c��B'y���s\de4�>H�NA���#4�6^�r�2�@-W���1�z��O�N�U�u�^���P܆�
T+�պ����.�['��j.֛BZ���㓫�QCyXQ�C9�ˣ�s����d��z&aW���n��cTi�Y������d{���(�?[�wz      �   �  x�M�Ko�0�ϓO���ֆ�:Z"*4�l)R���
�����o�c�J+����1 Gm�^��C��DQ�@�I!�qPf��q��������y/������@�����#�ip���	���jYm��Q1��O4���KLD�i�8�Y_4}�Rֿ�Q6�M:��!����͔�H�~���m�r���ج�MG�݈��Yk4��coŊ��ր�e�e�wL
Ǚ�XK��P\��c� If��+WA�y���-y3��}gohC�,���r�j�|�_.<Wɦn}�9t���O�kI������nT7^��Buuy����Ƒ���m�3���W7"�l�"�nx�U]z~�'8�!;(����@�Z��A[li�P��
-����܎b>�'�$	�i"+���=�V�՟%�p��^nU#N�i��q��ROf�S���?���j��O4�$      �   �   x����j�0E��Wx_�H��׷d�&����L��u�tB�)�ι����{���>��]�U�\ /�Q&΂��'�^@�E�H��ϒ�����9-�Z�~�O������ѿ��'��.;�":�#��6y�K?������}�|�`��F�D6%I��5��-d��u��1#d�,Ĕb���B�7�<��YB����d70�ؔ�Z��]��H�K@ngY���6�LO� �dK�B
O	a�t�h 6��"�ͼBԝ�Z��p�      �   $  x�m��n�0��ӧ�
��;�l���1K��N;e*5/x��F����O~n�:�Ցru �q�Lҷ������`4��83�.q���J74V�9�$�f�q^ġ��|��WՁ�/ʭiN���a:/�k��������q��9d�����l/�:�
��(`B&�O��J�ѵ�D�=�E.|��������n)_m��o� �)�d
q�=���X��!2���/4��M�uS^5���u�Hdk�3c0��[3s��252��a�t.Xt�>ad�?�����6-d-�����3�1"�� .#s      �      x��Z�n�H�}���PR�jI�mٺز�*0RdJL�d�x�J~�����/��IJ�V�w�jӼfD�8q"ҭ���G �Dy������a�=Y;�z�i5����]JQ�jU�n��t�ꕻJ���,P�+b��D*q[��2v���T$�\+��*�;r��i��Zk�k��3��"�?���w�:��N��I��?���"/�K�ǵ�y_-��.�W����g��2�-��5�_<8����5{νX�PK���-9��JK֩J��$z'�/n*�2^�/��T�2Jr��r��Z�GI7U��Ǆ��տ�u�w/ݚT�׺o��`>��w���e���;ͳV�yR���B�F��Į����CC7�"�W2�y=2Ҵq��F"v3)7d�{��ʓ�J��안T����j�A��b7)ҬP9=��E�X�|�|\<��^���<x�z����ݝ����v�i�����IK^F�sXp�p��`A(��k��J��(HU$�\���x݊@S�Fxd���
C2�0��b�.ܝHS�7��>;�9ش���l�R�=����k������r\[��ι�:�j'Bl�LEl��/���ԦA���&���G� ����3�]i,�l��Gx�n&�XI���X�&mS��`
d�ݝ�u
J��tx���3ű���f�7\�����N*0�u�$�Q����Ă�_v9�T�%*��Po�C�g2\�|�y���q]���у9�[Z��o�NײJ�P�d�D��{e��"�e�q�tk�n�5 &r���x�ȁCg�ɟ���_�,�ۅ�D�Ɇ1�^��U��������� .��ΝP�����p4��[O���H�\�m)�Ӓ  +�2��Uq��c_y"�e��f��M5�;�O�b�����Ϯ~h���M\������F���h�0p�,H�?\z��������fb�V��ǜ��Eqc�o-�2f>b����i��YT��!C�i�b/B��Sk�j�}8����*�z�)���h2􄁷y^�oy>]��j~��ᇿ��qQ�=p�ͳf��p�J84cB��� 7Sof�ڭ[S�Ġ�4�UE2��
g�6��+����&��5��
�K��D�?/�\*�ܑy�����S4�_������Y��<!�m���y���l�Hl����Zf,�"�UӿDj��
�\�����j5k��r�Zy��NOq�פ'��wO�CZxg�:f˙�VX���Թ��;�:�J��lR��%��ӺC�#Έ�d�Lh�X���P@�X���0$!B��$�T˙�L�#~�	p�'O1�������Ϗ�%S��w�?�̖q{Ro#��q��3������m ���i��d�>TY��6��%��H�"�F���2��i�$&��w�t��=��ϟ��������A�k�Fըq9y�Q������^���,B��VYc��y�S�:�^�K��_�0��I�����s�&��N#v�1�@�ȃQ�ʒ	�V�ğ���H�U*��#H6?��Z+� ~�5�m+�ZN�i��Ν�������Z�.�
�gApT�DU��$��RT$rX,i�$��E��n�Q����X7��� 1�Q*蹛����i��YѴҎ�j�Q򽦽\�%�4X}�K�>eHZ�uJ�V%:$��j�FL��h�f �Z�� � ag��x�7Ŧ�����C]��Q=�F�{?�#�K�Χ����fIb�Ƴ��ˎ� �@*���<_�$ܻ��*������P�	�V;�:AĲ�dQM֫��~�q�J��>���]ܐ��u4,���L@]�-V-�	����Ϗot�*�uG ��I�Xz]@���  u}�a
RYe�d4j�Hk���3�.��v�ʃ���r)	X��K��X�:j�d��*E?A����0蹀*|u��"UTE��>JW��K�\w�=u���YB8�K5>-*�*C~JAY��1����^!j@C)��𱚪��;���e���S�y��=z�8�v(ʯ���mt5j�Q�X��\$�	)#J�_�������p(��<	
C'l�ǺѳDc� =��zC��g�Ɋt��ǚ	���S�BA���G�i���ߗS�����<�x�����f��A3�;k7A)aXą;K�^��̒\�����ۍ���E%������P��5]��2Y������	�,��x�A���@�i�?U����Z_G*xf��x���d����C��_w���'�n����pF���c�j.����i�w�E�b@������Oӂ�r"�
�!�d}EL��=�u]���lO���:a��f���d���K2lv?�}��=��p�z���v)���0�p�ˉ���Ef�S��ɐO�hԏ
)�a��Ġ6��l���_�E�E��c��|$�z�1�7��"���>���1qZ�`t��V��>�y~Z+��U��e�;;|�Z�ǯL�`p�Q*�n�F-R@V�ʬx�/'O������@N��
����y�D&���� �S���M秕��Һ�g���
��D�}8���./:��8�o���岣���Ӧ��q���Q[�s�^��-k���=��X*S��}b��@��-���RDY� ��sE�ܥZq�P��-��J���[���j_�N8�U�!��?v7�m^��`�����1�����![ժ�)�%��19�Yi��T��e%�t$�j��q5.$5�w;�ijس�;��өV{�]\?��|}�)^��M[�i_���/Fs���y�$�HDX���������U�4;4C,íf(�l��E�b_(jX�H�r��*�h��<��0F�[��כ���nW^�����m�7+�b��u��݂��*��Z|��3���陃�&I�Ir�@j/&�YG���1���H䢣F3����Ej�b҃�6)��8n�2K�w"�
���ȂH�u^��1c*H�X�2x�]"|�*�K��BGK�7��ct�����T�}NX�*���Uk����#�h.Rhx�_�6j�FJh�A����sF�Z�d2���D�9y����P��z8��L��s�PT�d�n\�����9}�_�P��_��V���ݐ�FFf!egɋ3�~���6cCH�,�-gD��$�A���:ܲ
�e\K�+4J�,�Ê)Z.�t6>rE�q�a̵��*��_��(Eճ��[`t�={�rJ�7�8��� �G�aG�!in�rP����7S��w17fd:Ν
��H���qQ2#c���<m�
�I��(��'\@��N�����q|����F�ӽ�#t�?H���H��Ux��)Y.C��=U`hڐ�*�k���6�ke�Ú�A!l�*�?ӻt�M�v|�#|*J�_�����GF�܆[�̐����}C`���@��2�� b��'���x�h�!-�\�S�f���ٙ$��l3��]D���t�BlKAd�����h�^/�m6~c�w$����.�R���,��`��*q��g��@�R�2�mD@B�42�eZA�K���ށ Z�� wA�WPb:4Q����P gt�~:r�[�l���:�c/|��I�7��5�M�ds���Z�I���g|N~�^�d��dװ�N�!�}wv��&A�h��4��=����N�eXМQ�vn�PF%,n������hd9���e�(J�Q�PJA#.��Ҋeh����:�T��dF@<�ޢ:µ9�����+ �n�>�*�#���{��x�1�V��x���؝�%h����QЖ&8��@�]�qLd-�O�F�h�38��Ohbڭ��9'�k ,y�t� q� ��-�C����U����=S���q��}�G�Mк�gj�;;73��X���:whe2��u=�>U��\�V�J��K_��������P��7Rm�`j����->��f�Dc�F����p>�����4{��>\��TY�;�璪��hz:�v���<Ъ�?w&MC*��<_��/U��	��]&���3bI1#\����"�\���.'��+w�b�+s�yJg߲�)�.��Rʢ��㉞3�O�U{/�=��>2p�}�O����\.��� �  �C�M0��nOF�"���4cՒ�86��#?زgB�۷U9m*X5���4�#�25�˜�rT��306��[o��nei�y�z/����lº����fc�B�]���D]�W\�ˉ����Iq��*��$mPKY��R��mLeFCG���������m$Z�e�>�&���6�<��6��8�1B\M4@Է��L�iJxy��tTY�$<(^��I�BIzK��:7E�����+j�(&v���Y���o�f��w��L��&ñ���DbYw�_� g�l�6�V�a�m=�F�E���WM$aUm�� r614��LC2湢��U<�5k��8*5g}�eJ;'H}Z^��dǹ��a�4�f�\Q���.�7f��c�P���r�����h��h�5c�����^�H]D(
���d�58���1O�,m����h��/fj{�X���iD�N_a����U�u��O���(��]?;;�_L�w      �   1  x��[r1��aR�1ƾK���R�5=V<v3֍�2J9���Rǲ:�U��X����2��(W\�+l�;�Uל��𘣼�v�g2���V�hfr��Ѣ��ڤ��qz Q:~��l�����Պ�U&q兙�X���1��K�?���ܾL�h��<��;|�����'�9`�Y���l5n^���jܼK�9jL�&u�ŧ�1��q��O3��4�,K+�2����w�$O3ou�\:�j���,C����hXm[�IṦͧ���Ϙ�����̥���7�����e�wpt�h~�w�l��H��^�     
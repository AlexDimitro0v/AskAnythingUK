--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
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


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: main_area; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_area (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.main_area OWNER TO postgres;

--
-- Name: main_area_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_area_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_area_id_seq OWNER TO postgres;

--
-- Name: main_area_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_area_id_seq OWNED BY public.main_area.id;


--
-- Name: main_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_category (
    id integer NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.main_category OWNER TO postgres;

--
-- Name: main_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_category_id_seq OWNER TO postgres;

--
-- Name: main_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_category_id_seq OWNED BY public.main_category.id;


--
-- Name: main_feedbackercandidate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_feedbackercandidate (
    id integer NOT NULL,
    application character varying(300) NOT NULL,
    feedback_id integer NOT NULL,
    feedbacker_id integer NOT NULL
);


ALTER TABLE public.main_feedbackercandidate OWNER TO postgres;

--
-- Name: main_feedbackercandidate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_feedbackercandidate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_feedbackercandidate_id_seq OWNER TO postgres;

--
-- Name: main_feedbackercandidate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_feedbackercandidate_id_seq OWNED BY public.main_feedbackercandidate.id;


--
-- Name: main_feedbackercomments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_feedbackercomments (
    id integer NOT NULL,
    feedbacker_comments text NOT NULL
);


ALTER TABLE public.main_feedbackercomments OWNER TO postgres;

--
-- Name: main_feedbackercomments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_feedbackercomments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_feedbackercomments_id_seq OWNER TO postgres;

--
-- Name: main_feedbackercomments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_feedbackercomments_id_seq OWNED BY public.main_feedbackercomments.id;


--
-- Name: main_feedbackrequest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_feedbackrequest (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    maintext text NOT NULL,
    date_posted timestamp with time zone NOT NULL,
    date_started timestamp with time zone NOT NULL,
    date_completed timestamp with time zone NOT NULL,
    time_limit integer NOT NULL,
    reward integer NOT NULL,
    feedbacker_comments text NOT NULL,
    feedbacker_rated integer NOT NULL,
    area_id integer NOT NULL,
    feedbackee_id integer NOT NULL,
    feedbacker_id integer NOT NULL
);


ALTER TABLE public.main_feedbackrequest OWNER TO postgres;

--
-- Name: main_feedbackrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_feedbackrequest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_feedbackrequest_id_seq OWNER TO postgres;

--
-- Name: main_feedbackrequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_feedbackrequest_id_seq OWNED BY public.main_feedbackrequest.id;


--
-- Name: main_purchase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_purchase (
    id integer NOT NULL,
    "time" timestamp with time zone NOT NULL,
    is_completed integer NOT NULL,
    feedback_id integer NOT NULL,
    feedbackee_id integer NOT NULL,
    feedbacker_id integer NOT NULL
);


ALTER TABLE public.main_purchase OWNER TO postgres;

--
-- Name: main_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_purchase_id_seq OWNER TO postgres;

--
-- Name: main_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_purchase_id_seq OWNED BY public.main_purchase.id;


--
-- Name: main_rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_rating (
    id integer NOT NULL,
    date_posted timestamp with time zone NOT NULL,
    overall integer NOT NULL,
    quality integer NOT NULL,
    speed integer NOT NULL,
    communication integer NOT NULL,
    review text NOT NULL,
    feedbackee_id integer NOT NULL,
    feedbacker_id integer NOT NULL
);


ALTER TABLE public.main_rating OWNER TO postgres;

--
-- Name: main_rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_rating_id_seq OWNER TO postgres;

--
-- Name: main_rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_rating_id_seq OWNED BY public.main_rating.id;


--
-- Name: main_tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_tag (
    id integer NOT NULL,
    category_id integer NOT NULL,
    feedback_id integer NOT NULL
);


ALTER TABLE public.main_tag OWNER TO postgres;

--
-- Name: main_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_tag_id_seq OWNER TO postgres;

--
-- Name: main_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_tag_id_seq OWNED BY public.main_tag.id;


--
-- Name: users_specialism; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_specialism (
    id integer NOT NULL,
    category_id integer NOT NULL,
    feedbacker_id integer NOT NULL
);


ALTER TABLE public.users_specialism OWNER TO postgres;

--
-- Name: users_specialism_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_specialism_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_specialism_id_seq OWNER TO postgres;

--
-- Name: users_specialism_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_specialism_id_seq OWNED BY public.users_specialism.id;


--
-- Name: users_userprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_userprofile (
    id integer NOT NULL,
    city character varying(100) NOT NULL,
    description text NOT NULL,
    linkedin character varying(200) NOT NULL,
    url_link_1 character varying(200) NOT NULL,
    url_link_2 character varying(200) NOT NULL,
    url_link_3 character varying(200) NOT NULL,
    image character varying(100) NOT NULL,
    premium_ends timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.users_userprofile OWNER TO postgres;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_userprofile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_userprofile_id_seq OWNER TO postgres;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_userprofile_id_seq OWNED BY public.users_userprofile.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: main_area id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_area ALTER COLUMN id SET DEFAULT nextval('public.main_area_id_seq'::regclass);


--
-- Name: main_category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_category ALTER COLUMN id SET DEFAULT nextval('public.main_category_id_seq'::regclass);


--
-- Name: main_feedbackercandidate id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackercandidate ALTER COLUMN id SET DEFAULT nextval('public.main_feedbackercandidate_id_seq'::regclass);


--
-- Name: main_feedbackercomments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackercomments ALTER COLUMN id SET DEFAULT nextval('public.main_feedbackercomments_id_seq'::regclass);


--
-- Name: main_feedbackrequest id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackrequest ALTER COLUMN id SET DEFAULT nextval('public.main_feedbackrequest_id_seq'::regclass);


--
-- Name: main_purchase id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_purchase ALTER COLUMN id SET DEFAULT nextval('public.main_purchase_id_seq'::regclass);


--
-- Name: main_rating id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_rating ALTER COLUMN id SET DEFAULT nextval('public.main_rating_id_seq'::regclass);


--
-- Name: main_tag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tag ALTER COLUMN id SET DEFAULT nextval('public.main_tag_id_seq'::regclass);


--
-- Name: users_specialism id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_specialism ALTER COLUMN id SET DEFAULT nextval('public.users_specialism_id_seq'::regclass);


--
-- Name: users_userprofile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile ALTER COLUMN id SET DEFAULT nextval('public.users_userprofile_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add specialism	1	add_specialism
2	Can change specialism	1	change_specialism
3	Can delete specialism	1	delete_specialism
4	Can view specialism	1	view_specialism
5	Can add user profile	2	add_userprofile
6	Can change user profile	2	change_userprofile
7	Can delete user profile	2	delete_userprofile
8	Can view user profile	2	view_userprofile
9	Can add area	3	add_area
10	Can change area	3	change_area
11	Can delete area	3	delete_area
12	Can view area	3	view_area
13	Can add category	4	add_category
14	Can change category	4	change_category
15	Can delete category	4	delete_category
16	Can view category	4	view_category
17	Can add feedbacker candidate	5	add_feedbackercandidate
18	Can change feedbacker candidate	5	change_feedbackercandidate
19	Can delete feedbacker candidate	5	delete_feedbackercandidate
20	Can view feedbacker candidate	5	view_feedbackercandidate
21	Can add feedbacker comments	6	add_feedbackercomments
22	Can change feedbacker comments	6	change_feedbackercomments
23	Can delete feedbacker comments	6	delete_feedbackercomments
24	Can view feedbacker comments	6	view_feedbackercomments
25	Can add feedback request	7	add_feedbackrequest
26	Can change feedback request	7	change_feedbackrequest
27	Can delete feedback request	7	delete_feedbackrequest
28	Can view feedback request	7	view_feedbackrequest
29	Can add purchase	8	add_purchase
30	Can change purchase	8	change_purchase
31	Can delete purchase	8	delete_purchase
32	Can view purchase	8	view_purchase
33	Can add rating	9	add_rating
34	Can change rating	9	change_rating
35	Can delete rating	9	delete_rating
36	Can view rating	9	view_rating
37	Can add tag	10	add_tag
38	Can change tag	10	change_tag
39	Can delete tag	10	delete_tag
40	Can view tag	10	view_tag
41	Can add log entry	11	add_logentry
42	Can change log entry	11	change_logentry
43	Can delete log entry	11	delete_logentry
44	Can view log entry	11	view_logentry
45	Can add permission	12	add_permission
46	Can change permission	12	change_permission
47	Can delete permission	12	delete_permission
48	Can view permission	12	view_permission
49	Can add group	13	add_group
50	Can change group	13	change_group
51	Can delete group	13	delete_group
52	Can view group	13	view_group
53	Can add user	14	add_user
54	Can change user	14	change_user
55	Can delete user	14	delete_user
56	Can view user	14	view_user
57	Can add content type	15	add_contenttype
58	Can change content type	15	change_contenttype
59	Can delete content type	15	delete_contenttype
60	Can view content type	15	view_contenttype
61	Can add session	16	add_session
62	Can change session	16	change_session
63	Can delete session	16	delete_session
64	Can view session	16	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	argon2$argon2i$v=19$m=512,t=2,p=2$dW9aQUVUVmdPanA4$nPDJvgHwLtxf38g48LNecQ	2020-02-03 21:57:19+00	t	admin			askanything.admin@mail.com	t	t	2020-02-03 20:31:00+00
3	argon2$argon2i$v=19$m=512,t=2,p=2$cEU3MFlFT3ZOalZw$ApLGOSjhSYQgNh+y73zNNA	2020-02-03 22:14:55.103957+00	f	stepan	s	b	askanything.stepan@mail.com	f	t	2020-02-03 20:32:07+00
2	argon2$argon2i$v=19$m=512,t=2,p=2$NFhnNXk0eWVPdVJ3$jtyewPxedMH9CqeDuXofmQ	2020-02-03 22:18:21.867703+00	f	lukas	l	a	askanything.lukas@mail.com	f	t	2020-02-03 20:31:41+00
6	argon2$argon2i$v=19$m=512,t=2,p=2$bGdHMEJndmhGZmlK$WBLABtu+6Hflv6luyWRUWA	2020-02-03 22:18:40.668281+00	f	niven	n	t	askanything.niven@mail.com	f	t	2020-02-03 20:33:24+00
4	argon2$argon2i$v=19$m=512,t=2,p=2$TmNWckRYZDBZOXpN$VAjw+pr3PVrGueOpr0HM7Q	2020-02-03 22:19:12.350685+00	f	alex	a	d	askanything.alex@mail.com	f	t	2020-02-03 20:32:35+00
5	argon2$argon2i$v=19$m=512,t=2,p=2$TkdHMEhNNVdGTGVK$AVmTU0tpDTVAZcZRUNYTsA	2020-02-03 22:19:28.587293+00	f	robert	r	r	askanything.robert@mail.com	f	t	2020-02-03 20:32:57+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2020-02-03 20:31:41.155957+00	2	lukas	1	[{"added": {}}]	14	1
2	2020-02-03 20:31:56.467959+00	2	lukas	2	[{"changed": {"fields": ["first_name", "last_name", "email"]}}]	14	1
3	2020-02-03 20:32:07.938396+00	3	stepan	1	[{"added": {}}]	14	1
4	2020-02-03 20:32:16.669524+00	3	stepan	2	[{"changed": {"fields": ["first_name", "last_name", "email"]}}]	14	1
5	2020-02-03 20:32:35.046903+00	4	alex	1	[{"added": {}}]	14	1
6	2020-02-03 20:32:46.024942+00	4	alex	2	[{"changed": {"fields": ["first_name", "last_name", "email"]}}]	14	1
7	2020-02-03 20:32:57.806696+00	5	robert	1	[{"added": {}}]	14	1
8	2020-02-03 20:33:10.130502+00	5	robert	2	[{"changed": {"fields": ["first_name", "last_name", "email"]}}]	14	1
9	2020-02-03 20:33:24.18824+00	6	niven	1	[{"added": {}}]	14	1
10	2020-02-03 20:33:42.320927+00	6	niven	2	[{"changed": {"fields": ["first_name", "last_name", "email"]}}]	14	1
11	2020-02-03 20:33:57.260081+00	4	alex	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
12	2020-02-03 20:34:07.031802+00	2	lukas	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
13	2020-02-03 20:34:18.558903+00	5	robert	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
14	2020-02-03 20:34:30.33137+00	3	stepan	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
15	2020-02-03 20:35:35.175217+00	3	stepan	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
16	2020-02-03 20:35:46.931661+00	3	stepan	2	[{"changed": {"fields": ["password"]}}]	14	1
17	2020-02-03 20:35:55.336225+00	5	robert	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
18	2020-02-03 20:36:00.63669+00	6	niven	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
19	2020-02-03 20:36:06.106787+00	2	lukas	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
20	2020-02-03 20:36:11.115404+00	4	alex	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	14	1
21	2020-02-03 21:57:29.756716+00	1	admin	2	[{"changed": {"fields": ["email"]}}]	14	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	users	specialism
2	users	userprofile
3	main	area
4	main	category
5	main	feedbackercandidate
6	main	feedbackercomments
7	main	feedbackrequest
8	main	purchase
9	main	rating
10	main	tag
11	admin	logentry
12	auth	permission
13	auth	group
14	auth	user
15	contenttypes	contenttype
16	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-02-03 20:30:17.872211+00
2	auth	0001_initial	2020-02-03 20:30:18.015801+00
3	admin	0001_initial	2020-02-03 20:30:18.0537+00
4	admin	0002_logentry_remove_auto_add	2020-02-03 20:30:18.06168+00
5	admin	0003_logentry_add_action_flag_choices	2020-02-03 20:30:18.06967+00
6	contenttypes	0002_remove_content_type_name	2020-02-03 20:30:18.087636+00
7	auth	0002_alter_permission_name_max_length	2020-02-03 20:30:18.093593+00
8	auth	0003_alter_user_email_max_length	2020-02-03 20:30:18.103567+00
9	auth	0004_alter_user_username_opts	2020-02-03 20:30:18.110548+00
10	auth	0005_alter_user_last_login_null	2020-02-03 20:30:18.119526+00
11	auth	0006_require_contenttypes_0002	2020-02-03 20:30:18.122516+00
12	auth	0007_alter_validators_add_error_messages	2020-02-03 20:30:18.130495+00
13	auth	0008_alter_user_username_max_length	2020-02-03 20:30:18.14745+00
14	auth	0009_alter_user_last_name_max_length	2020-02-03 20:30:18.158421+00
15	main	0001_initial	2020-02-03 20:30:18.38681+00
16	sessions	0001_initial	2020-02-03 20:30:18.410752+00
17	users	0001_initial	2020-02-03 20:30:18.475575+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
l80z9qakudea9s1csda4cs1lr35fxsq1	ZDQ1NzEwNTY3ZWFhZGU1MTY4NDQ3ZTllYTQ2NDJmMmYwNWE5ZjE3NTp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxYzNhNjA0YjUzMjA4ZmM2ZjhhMzEzMjI5N2NlNzJmY2ZhZTBkZGYzIn0=	2020-02-17 22:19:28.592311+00
\.


--
-- Data for Name: main_area; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_area (id, name) FROM stdin;
1	Video & Animation
2	Graphics & Design
3	Writing
4	Translation
5	Technology
6	Music & Audio
\.


--
-- Data for Name: main_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_category (id, name) FROM stdin;
1	3D
2	Painting
3	Bug
4	Python
5	Horror
6	Novel
7	Violin
8	Mandarin
9	Assingment
10	University
11	Java
12	Shadows
13	Engineering
14	CV
15	Writing
16	Coding
17	Composing
18	EnglishToGerman
19	German
20	Story
21	Project
22	White
23	Black
24	Pencin
25	GIF
26	Wallpaper
27	Song
28	Colouring
29	Animation
30	Video
31	Pencil
32	Computing
33	Code
34	C  
35	Expensive
36	Long
37	BigMoney
38	Website
39	Django
40	Short
41	Photoshop
42	Ghost
43	sdfdsf
44	afddsf
45	sdfsdf
46	FrenchToEnglish
47	French
48	Electronics
49	Piano
50	SDAK:SFKJ:SAF
51	ASDfnafalSAD
52	Wafnfkna
\.


--
-- Data for Name: main_feedbackercandidate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_feedbackercandidate (id, application, feedback_id, feedbacker_id) FROM stdin;
1	Best	35	3
2	Blah	27	3
3	Yo	5	3
\.


--
-- Data for Name: main_feedbackercomments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_feedbackercomments (id, feedbacker_comments) FROM stdin;
\.


--
-- Data for Name: main_feedbackrequest; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_feedbackrequest (id, title, maintext, date_posted, date_started, date_completed, time_limit, reward, feedbacker_comments, feedbacker_rated, area_id, feedbackee_id, feedbacker_id) FROM stdin;
1	3D Painting	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla lacinia arcu vel consequat maximus. Pellentesque interdum accumsan purus, vitae consectetur mi gravida eu. Sed dapibus risus sed nisl cursus tincidunt. Sed nec ex et ipsum elementum cursus nec quis mauris. Ut tristique leo eget eleifend iaculis. Nulla facilisi. Vestibulum eu lobortis dolor. Morbi in velit magna. Sed vehicula sapien ut metus egestas, at feugiat dolor sodales. Sed semper ipsum id arcu aliquam semper. Proin finibus.	2020-02-03 20:39:51.621112+00	2020-02-03 20:39:51.621112+00	2020-02-03 20:39:51.621112+00	7	35		0	2	2	2
3	Horror Novel	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed egestas mattis ante, cursus ullamcorper nisl fermentum posuere. Sed a sem lorem. Cras et mauris imperdiet massa malesuada dapibus. Vivamus feugiat sapien et est tristique ornare. Morbi ut tellus in eros blandit ornare. Nullam imperdiet nisl nec dolor sagittis facilisis. Maecenas ac placerat risus, eu rutrum leo. Phasellus ut pharetra lorem, et vestibulum nisi. Donec facilisis in metus a eleifend. Curabitur metus ipsum, aliquet eu efficitur.	2020-02-03 20:41:47.781083+00	2020-02-03 20:41:47.781083+00	2020-02-03 20:41:47.781083+00	5	300		0	3	2	2
4	Bug Fix Python	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis mattis purus, vel convallis massa. Curabitur placerat metus risus, eget porta libero ultrices non. Phasellus elementum gravida lobortis. Duis ante orci, pretium in rhoncus ac, vulputate vitae diam. Nunc vitae feugiat arcu. Nullam ex massa, mollis non volutpat ut, eleifend non felis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Suspendisse massa purus, varius et mi non, posuere efficitur sapien.	2020-02-03 20:43:36.846149+00	2020-02-03 20:43:36.846149+00	2020-02-03 20:43:36.846149+00	20	69		0	5	2	2
6	Mandarin University Assingment	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin id varius mauris. Nunc at placerat sapien, id hendrerit lorem. Etiam enim dui, malesuada eu bibendum a, commodo a nunc. Proin fringilla risus a turpis condimentum, quis maximus augue posuere. Praesent maximus, lectus sit amet volutpat volutpat, nisl libero tempus nisi, sed tincidunt magna lectus sit amet orci. Nullam consequat neque at vestibulum accumsan. Fusce eu tortor aliquam, dignissim tellus non, pharetra leo. Nulla efficitur nibh.	2020-02-03 20:45:16.979914+00	2020-02-03 20:45:16.979914+00	2020-02-03 20:45:16.979914+00	6	35		0	4	2	2
7	Java Code	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eget venenatis diam. Sed vehicula blandit eros vel lobortis. Nullam in aliquam lectus, eget sollicitudin felis. Maecenas fringilla nunc ante, vitae pulvinar nisi congue id. Suspendisse a varius nibh. Ut quis faucibus metus. Nullam facilisis odio non augue vehicula, id elementum dui auctor. Proin gravida enim ut est luctus, eu semper eros pretium. Praesent ipsum justo, egestas id tincidunt ac, blandit et odio. Nunc vel nisi.	2020-02-03 20:46:21.004763+00	2020-02-03 20:46:21.004763+00	2020-02-03 20:46:21.004763+00	10	100		0	5	2	2
8	Fixing Shadows	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et sem at risus luctus hendrerit. Sed in interdum enim, in interdum ante. Mauris a pellentesque nibh. Duis ultrices eleifend mattis. Donec sed accumsan diam, et dignissim nisl. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum tincidunt tellus id ex euismod, in imperdiet mi eleifend. Nulla ac rutrum nibh, vitae mollis arcu. Quisque a vestibulum lorem. Donec a sollicitudin nisi. Cras non nisl ut mi.	2020-02-03 20:50:29.930584+00	2020-02-03 20:50:29.930584+00	2020-02-03 20:50:29.930584+00	2	30		0	1	3	3
9	My Animation	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin quam neque, sagittis id pulvinar vitae, viverra a metus. Proin id ex velit. Suspendisse potenti. Pellentesque at tellus ultricies, ultricies mauris vel, venenatis orci. Integer gravida cursus tortor. Proin ut mi lorem. Nulla scelerisque auctor ipsum, id lacinia orci egestas vel.\r\n\r\nUt maximus arcu vel nulla luctus molestie. Aenean aliquam elit ac mauris sodales, et molestie mauris ultricies. Mauris ante quam, vulputate quis velit vel, volutpat.	2020-02-03 20:51:34.807512+00	2020-02-03 20:51:34.807512+00	2020-02-03 20:51:34.807512+00	10	30		0	1	3	3
10	Engineering CV	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque tincidunt malesuada nisi, a bibendum neque dapibus hendrerit. Sed et arcu magna. Curabitur rutrum, purus et efficitur pharetra, nisi metus scelerisque purus, et pharetra est ligula sit amet nulla. Phasellus velit eros, varius vel risus at, feugiat venenatis ex. Nulla lectus felis, placerat at congue quis, mattis sit amet enim. Nam pellentesque quam sed purus maximus, non vestibulum magna viverra. Donec vitae libero et nisl aliquam.	2020-02-03 20:54:37.788358+00	2020-02-03 20:54:37.788358+00	2020-02-03 20:54:37.788358+00	9	45		0	3	3	3
12	Composing Music	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi nec metus nisi. Duis et volutpat mi, in elementum purus. Curabitur dapibus nec urna sit amet blandit. Maecenas volutpat arcu eu lorem rhoncus, id consectetur quam scelerisque. Integer id nisl massa. Nullam laoreet accumsan velit ut accumsan. Nullam metus lorem, tincidunt eget nulla ut, vehicula dignissim lacus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vitae fringilla magna. In gravida feugiat vulputate. Vestibulum ultrices erat.	2020-02-03 20:58:56.250245+00	2020-02-03 20:58:56.250245+00	2020-02-03 20:58:56.250245+00	13	55		0	6	3	3
13	MyDesing Project	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam quis mattis metus. Ut sit amet ligula quis nunc vulputate gravida. Donec aliquet auctor nunc et bibendum. Phasellus vel elit nunc. Proin ut mattis eros, quis imperdiet nisl. Vestibulum pharetra ante et tortor mollis tristique. Integer placerat nec libero id semper. Duis condimentum egestas orci, eu mollis nisl auctor id. Sed feugiat at risus posuere dictum. In hac habitasse platea dictumst. Aliquam accumsan condimentum ligula, id.	2020-02-03 21:03:20.74891+00	2020-02-03 21:03:20.749907+00	2020-02-03 21:03:20.749907+00	15	150		0	2	3	3
15	Black and White	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sed pretium nunc, rhoncus faucibus nulla. Donec pretium turpis at diam eleifend venenatis. Etiam nec metus faucibus, imperdiet arcu ac, convallis tortor. Donec at turpis scelerisque, congue ante id, finibus massa. Vivamus bibendum ex ac neque efficitur, ut dapibus turpis porta. Nunc sollicitudin luctus metus, quis vulputate dui dictum quis. Cras nec diam ante. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos.	2020-02-03 21:08:54.259013+00	2020-02-03 21:08:54.259013+00	2020-02-03 21:08:54.259013+00	14	20		0	2	4	4
5	Violin	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc molestie in dolor id ultricies. Aliquam erat volutpat. Maecenas quis felis ut odio eleifend vulputate. Sed aliquam posuere diam, vel pretium lorem mollis rhoncus. Fusce sed mi leo. Nam venenatis, libero nec bibendum mattis, eros dui sagittis urna, nec rutrum tellus tortor quis augue. Vivamus vel nisl ligula. Vestibulum viverra semper bibendum. Nulla eros dolor, cursus et turpis eu, iaculis maximus nulla. Pellentesque dui velit, iaculis.	2020-02-03 20:44:27.848896+00	2020-02-03 22:02:05.079627+00	2020-02-03 22:10:11.986735+00	10	10	test test test	1	6	2	3
16	Animated Wallpapers	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus eget est iaculis leo sollicitudin vestibulum. Nam nec dui nunc. Suspendisse elementum dolor libero. Nulla mollis hendrerit fermentum. Nullam vestibulum gravida tortor, ut vestibulum tortor dignissim id. Integer auctor elit dignissim odio consequat semper. Etiam at urna malesuada, volutpat nunc sed, venenatis quam. Vivamus nec lorem risus. Nullam eu venenatis massa. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed pulvinar.	2020-02-03 21:09:39.923181+00	2020-02-03 21:09:39.923181+00	2020-02-03 21:09:39.923181+00	16	66		0	1	4	4
17	Java Code	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer commodo diam leo, ac consequat tortor maximus ac. Maecenas eros nulla, viverra at felis in, rutrum hendrerit dui. Nulla interdum quam id arcu sagittis, in finibus ante hendrerit. Aenean condimentum felis et elit gravida, et venenatis libero egestas. Ut vulputate eleifend ex, id rutrum quam euismod non. Nulla elementum quis turpis sed elementum. Aliquam scelerisque ligula eget eros eleifend bibendum. Nunc pharetra varius erat in euismod.	2020-02-03 21:10:14.073491+00	2020-02-03 21:10:14.073491+00	2020-02-03 21:10:14.073491+00	7	50		0	5	4	4
18	Song Writing	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ac luctus ipsum, non pretium eros. Duis non ipsum quis est interdum faucibus. Nulla sed condimentum lorem. Suspendisse consectetur a nulla at varius. Morbi venenatis augue eget neque imperdiet rutrum. Cras pharetra porta magna, ac cursus augue porttitor et. Quisque sed urna vitae arcu lobortis dictum. In hac habitasse platea dictumst. Etiam vestibulum turpis vel felis ullamcorper feugiat. Ut suscipit pharetra elit, vitae malesuada metus sagittis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ac luctus ipsum, non pretium eros. Duis non ipsum quis est interdum faucibus. Nulla sed condimentum lorem. Suspendisse consectetur a nulla at varius. Morbi venenatis augue eget neque imperdiet rutrum. Cras pharetra porta magna, ac cursus augue porttitor et. Quisque sed urna vitae arcu lobortis dictum. In hac habitasse platea dictumst. Etiam vestibulum turpis vel felis ullamcorper feugiat. Ut suscipit pharetra elit, vitae malesuada metus sagittis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ac luctus ipsum, non pretium eros. Duis non ipsum quis est interdum faucibus. Nulla sed condimentum lorem. Suspendisse consectetur a nulla at varius. Morbi venenatis augue eget neque imperdiet rutrum. Cras pharetra porta magna, ac cursus augue porttitor et. Quisque sed urna vitae arcu lobortis dictum. In hac habitasse platea dictumst. Etiam vestibulum turpis vel felis ullamcorper feugiat. Ut suscipit phar.	2020-02-03 21:11:28.743324+00	2020-02-03 21:11:28.743324+00	2020-02-03 21:11:28.743324+00	15	130		0	3	4	4
19	Help with Colouring	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum in metus porta, pulvinar nisl ac, tristique ipsum. Morbi porta tortor felis. In non rhoncus dui, eget placerat mi. Ut imperdiet massa non nunc feugiat ultricies. Cras sit amet eros sem. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin pellentesque luctus ullamcorper. Maecenas pretium vestibulum tellus eu egestas. Aenean sit amet fermentum tellus, sit amet ultrices neque. Curabitur dictum maximus nulla a suscipit. Etiam tincidunt.	2020-02-03 21:12:29.975445+00	2020-02-03 21:12:29.975445+00	2020-02-03 21:12:29.975445+00	7	30		0	1	4	4
20	Pencil	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum et dictum magna. Phasellus rhoncus varius lectus et mattis. Donec vehicula justo quam, in tincidunt quam iaculis ac. Curabitur congue velit sit amet ipsum congue cursus. Proin auctor lorem ut pharetra pharetra. Praesent sagittis odio ut mi faucibus rutrum. Sed eu convallis risus. Aenean lobortis dui non enim ullamcorper, sed facilisis ipsum tincidunt. Duis non nisi interdum, semper est sit amet, suscipit lectus. Nunc cursus augue.	2020-02-03 21:13:06.451437+00	2020-02-03 21:13:06.451437+00	2020-02-03 21:13:06.451437+00	20	40		0	2	4	4
21	Short Story to German	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc quis felis feugiat, efficitur nisi nec, iaculis velit. Pellentesque massa est, accumsan id est semper, mollis eleifend nunc. Aliquam convallis erat quam, sed rhoncus lectus sodales vel. Sed pharetra turpis nec leo tincidunt, at dignissim massa malesuada. Sed et convallis augue, at sagittis purus. In libero augue, mattis a venenatis et, scelerisque vel ante. Integer sollicitudin blandit laoreet. Phasellus eu risus a mi viverra pellentesque. Duis.	2020-02-03 21:15:55.862741+00	2020-02-03 21:15:55.862741+00	2020-02-03 21:15:55.862741+00	12	33		0	4	3	3
22	Shadows	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas accumsan ipsum et dictum porttitor. Donec rutrum, ex at suscipit bibendum, odio turpis bibendum nisi, quis dapibus sapien dolor ut ipsum. Suspendisse mollis neque vitae magna ornare pellentesque. Praesent in bibendum purus. Etiam a elementum quam, eget convallis ligula. Morbi posuere diam quis nulla euismod placerat. Ut vitae lectus eget arcu sagittis sodales. Proin molestie mauris in ligula iaculis ultrices. Morbi consectetur eros eget diam volutpat.	2020-02-03 21:18:28.222377+00	2020-02-03 21:18:28.222377+00	2020-02-03 21:18:28.222377+00	14	30		0	2	5	5
23	Computing CV	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut congue ante et turpis laoreet vehicula. Sed rutrum in arcu vitae ullamcorper. Duis feugiat vel nibh sed porttitor. Nunc vulputate magna sit amet fermentum pretium. Mauris tellus odio, tristique sit amet enim eget, blandit cursus ipsum. Aliquam vitae tellus eu sapien ultricies venenatis et at turpis. Curabitur egestas mi ullamcorper turpis mollis vestibulum. Integer sit amet malesuada diam, at finibus nisl. Quisque non augue pharetra, ullamcorper.	2020-02-03 21:19:02.538937+00	2020-02-03 21:19:02.538937+00	2020-02-03 21:19:02.538937+00	5	100		0	3	5	5
24	Code in C++	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam pharetra, nisi id convallis vehicula, erat massa pharetra lectus, ac facilisis risus odio eget metus. Mauris interdum libero eu mauris lacinia condimentum. Suspendisse convallis risus massa, vehicula maximus sem feugiat vel. Maecenas rhoncus maximus dui, id convallis nisi tincidunt nec. Fusce euismod hendrerit nisl, nec tempus lacus. Pellentesque ac lectus non nibh feugiat tempor in nec magna. In ut ornare ante, in consequat diam. Pellentesque eu.	2020-02-03 21:19:53.321078+00	2020-02-03 21:19:53.321078+00	2020-02-03 21:19:53.321078+00	4	70		0	5	5	5
25	Engineering Project	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur congue sapien et erat pharetra, vel faucibus lorem ultricies. Integer vel hendrerit dolor. Phasellus justo ligula, eleifend in volutpat hendrerit, pellentesque at magna. Proin rhoncus posuere lacus et blandit. Aenean et turpis libero. Ut dignissim consequat nibh nec porttitor. Morbi eleifend, massa ac convallis luctus, tortor neque dignissim metus, in pharetra lorem magna non turpis. Aenean et placerat nisi. Aliquam rhoncus, nibh sed molestie tincidunt, risus.	2020-02-03 21:21:11.212775+00	2020-02-03 21:21:11.212775+00	2020-02-03 21:21:11.212775+00	40	990		0	5	5	5
26	Django Website	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas at vestibulum dolor, vel interdum lectus. Quisque dui nisi, blandit ac tincidunt non, faucibus a sapien. Proin et sapien ac purus egestas gravida ut eu metus. Sed sed ligula metus. Aliquam vel dolor a purus vestibulum rutrum. Vivamus eget ligula viverra, ultrices orci quis, interdum ligula. Nam vel dui ac nisl cursus suscipit. Pellentesque iaculis dui enim, eget tristique nisl mollis at. Vestibulum orci ligula, pulvinar.	2020-02-03 21:21:56.375458+00	2020-02-03 21:21:56.375458+00	2020-02-03 21:21:56.375458+00	9	80		0	5	5	5
27	Composition	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum bibendum hendrerit purus id pharetra. Mauris pharetra sed nulla quis convallis. Suspendisse varius sed ante nec rhoncus. Donec at arcu ultrices neque placerat condimentum. Morbi vitae felis eget ante semper dapibus nec non lacus. Suspendisse aliquam et dui vel feugiat. Ut id lacinia velit. Pellentesque placerat nunc et diam congue, nec hendrerit leo rhoncus. Aliquam congue hendrerit lorem, vitae pretium tellus commodo quis. Vivamus eu ligula.	2020-02-03 21:22:30.165169+00	2020-02-03 21:22:30.165169+00	2020-02-03 21:22:30.165169+00	10	60		0	6	5	5
28	Short 3D Movie	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac massa fringilla, mollis tellus id, ullamcorper est. Etiam luctus porttitor urna, a dictum nisi finibus ac. Aliquam faucibus porta turpis a sodales. Vestibulum rutrum magna eu ante consequat lobortis. Curabitur ac ex eu enim sagittis feugiat. Nunc tristique odio quam, sed tristique elit pharetra quis. Duis arcu purus, hendrerit vitae sodales eget, tristique ac lacus. Donec efficitur sed quam id efficitur. Ut vestibulum urna vitae.	2020-02-03 21:25:37.625337+00	2020-02-03 21:25:37.625337+00	2020-02-03 21:25:37.625337+00	7	50		0	1	6	6
29	Photoshop	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis vehicula ligula neque, vel dapibus tellus semper sit amet. Nam auctor nibh vel est tempor, non rhoncus erat accumsan. Quisque at placerat felis. Nam molestie ligula odio, quis sodales neque molestie id. Donec vitae lacinia neque. Nam placerat pretium massa, at semper arcu sollicitudin condimentum. Nam tortor turpis, efficitur at convallis fringilla, laoreet vitae sem. Pellentesque maximus, dolor id mattis luctus, mauris mi gravida est, sit.	2020-02-03 21:26:10.93922+00	2020-02-03 21:26:10.93922+00	2020-02-03 21:26:10.93922+00	3	30		0	2	6	6
30	Short Ghost Story	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed mollis risus sem, quis venenatis nibh commodo id. Duis nunc leo, fermentum vel justo nec, bibendum porttitor odio. Phasellus vel ligula non neque efficitur tempor et eu purus. Cras a justo sit amet urna suscipit tincidunt non et nisl. In imperdiet diam at elementum dignissim. Fusce ac lectus ante. Fusce egestas ex at nisi consectetur, eu luctus sapien bibendum. Praesent scelerisque sed ex quis venenatis. Suspendisse.	2020-02-03 21:26:49.714722+00	2020-02-03 21:26:49.714722+00	2020-02-03 21:26:49.714722+00	6	35		0	3	6	6
32	CV to French	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc interdum dui a lorem vestibulum ornare. Sed condimentum eget ex vitae vestibulum. Suspendisse eros elit, consectetur vel laoreet finibus, semper in sapien. Sed sit amet tristique purus. Sed porta mi id rutrum egestas. Nulla facilisi. Morbi fermentum libero velit, id euismod turpis lobortis a. Vestibulum faucibus dictum nisl id viverra. Suspendisse aliquam semper elit, in lobortis velit laoreet id. Praesent mattis semper nunc, volutpat tempor elit.	2020-02-03 21:32:10.817421+00	2020-02-03 21:32:10.817421+00	2020-02-03 21:32:10.817421+00	5	60		0	4	6	6
33	Electronics Project	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac purus tempor, tincidunt nisi non, ultrices nulla. Nullam volutpat odio in enim laoreet euismod non lobortis ipsum. Integer id dui sed dolor sagittis rutrum sit amet at nisi. Praesent congue varius consectetur. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nullam porttitor auctor diam. Aenean ac viverra arcu. Proin non nisl vel ipsum rutrum accumsan. Integer eget augue sed nunc.	2020-02-03 21:35:32.765319+00	2020-02-03 21:35:32.765319+00	2020-02-03 21:35:32.765319+00	7	75		0	5	6	6
35	Piano	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec egestas nunc in feugiat elementum. In finibus placerat elementum. In hac habitasse platea dictumst. Phasellus facilisis, mi eget pharetra tristique, neque metus aliquam quam, vel interdum nibh urna eget leo. Aenean iaculis ullamcorper accumsan. Aenean auctor dignissim eleifend. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Integer fermentum mi vel dictum iaculis. In ac egestas ante. Proin sed ante tristique, tristique ante.	2020-02-03 21:38:34.392727+00	2020-02-03 22:14:12.174611+00	2020-02-03 21:38:34.392727+00	5	55		0	6	6	3
\.


--
-- Data for Name: main_purchase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_purchase (id, "time", is_completed, feedback_id, feedbackee_id, feedbacker_id) FROM stdin;
1	2020-02-03 22:02:05.148443+00	1	5	2	3
2	2020-02-03 22:14:12.229438+00	0	35	6	3
\.


--
-- Data for Name: main_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_rating (id, date_posted, overall, quality, speed, communication, review, feedbackee_id, feedbacker_id) FROM stdin;
1	2020-02-03 22:10:48.249024+00	5	5	5	5	Best	2	3
\.


--
-- Data for Name: main_tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_tag (id, category_id, feedback_id) FROM stdin;
1	1	1
2	2	1
5	5	3
6	6	3
7	3	4
8	4	4
9	7	5
10	8	6
11	9	6
12	10	6
13	11	7
14	12	8
15	13	10
16	14	10
20	17	12
21	21	13
24	22	15
25	23	15
26	24	15
27	25	16
28	26	16
29	11	17
30	16	17
31	27	18
32	28	19
33	29	19
34	30	19
35	31	20
36	18	21
37	19	21
38	20	21
39	12	22
40	32	23
41	14	23
42	16	23
43	33	24
44	34	24
45	21	25
46	35	25
47	36	25
48	13	25
49	37	25
50	38	26
51	39	26
52	4	26
53	1	28
54	40	28
55	41	29
56	42	30
57	20	30
61	46	32
62	14	32
63	47	32
64	21	33
65	48	33
67	49	35
\.


--
-- Data for Name: users_specialism; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_specialism (id, category_id, feedbacker_id) FROM stdin;
7	15	3
8	16	3
9	17	3
\.


--
-- Data for Name: users_userprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_userprofile (id, city, description, linkedin, url_link_1, url_link_2, url_link_3, image, premium_ends, user_id) FROM stdin;
3	Aberdeen	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae mauris et sapien commodo pulvinar. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce viverra, arcu at laoreet consectetur, nibh enim gravida sapien, at tempus sem ligula et mauris. Aliquam aliquam ipsum enim, sed vulputate mi scelerisque vitae. Nam pharetra ultrices est, et scelerisque odio finibus a.\r\n\r\nPhasellus convallis, elit eu aliquam vehicula, diam massa elementum mauris, id varius metus ex.	http://linkedin.com	http://youtube.com	http://facebook.com		profile_pics/589989.jpg	2020-03-03 20:36:41.134665+00	3
2							default.jpg	2020-02-03 20:31:41.152947+00	2
6							default.jpg	2020-02-03 20:33:24.186271+00	6
4							default.jpg	2020-02-03 20:32:35.044909+00	4
5							default.jpg	2020-02-03 20:32:57.803704+00	5
1							default.jpg	2020-02-03 20:31:00.185284+00	1
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 64, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 6, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 21, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 16, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 17, true);


--
-- Name: main_area_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_area_id_seq', 6, true);


--
-- Name: main_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_category_id_seq', 52, true);


--
-- Name: main_feedbackercandidate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_feedbackercandidate_id_seq', 3, true);


--
-- Name: main_feedbackercomments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_feedbackercomments_id_seq', 1, false);


--
-- Name: main_feedbackrequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_feedbackrequest_id_seq', 36, true);


--
-- Name: main_purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_purchase_id_seq', 2, true);


--
-- Name: main_rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_rating_id_seq', 1, true);


--
-- Name: main_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_tag_id_seq', 72, true);


--
-- Name: users_specialism_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_specialism_id_seq', 9, true);


--
-- Name: users_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_userprofile_id_seq', 6, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: main_area main_area_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_area
    ADD CONSTRAINT main_area_pkey PRIMARY KEY (id);


--
-- Name: main_category main_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_category
    ADD CONSTRAINT main_category_pkey PRIMARY KEY (id);


--
-- Name: main_feedbackercandidate main_feedbackercandidate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackercandidate
    ADD CONSTRAINT main_feedbackercandidate_pkey PRIMARY KEY (id);


--
-- Name: main_feedbackercomments main_feedbackercomments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackercomments
    ADD CONSTRAINT main_feedbackercomments_pkey PRIMARY KEY (id);


--
-- Name: main_feedbackrequest main_feedbackrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackrequest
    ADD CONSTRAINT main_feedbackrequest_pkey PRIMARY KEY (id);


--
-- Name: main_purchase main_purchase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_purchase
    ADD CONSTRAINT main_purchase_pkey PRIMARY KEY (id);


--
-- Name: main_rating main_rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_rating
    ADD CONSTRAINT main_rating_pkey PRIMARY KEY (id);


--
-- Name: main_tag main_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tag
    ADD CONSTRAINT main_tag_pkey PRIMARY KEY (id);


--
-- Name: users_specialism users_specialism_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_specialism
    ADD CONSTRAINT users_specialism_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: main_feedbackercandidate_feedback_id_8749740e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_feedbackercandidate_feedback_id_8749740e ON public.main_feedbackercandidate USING btree (feedback_id);


--
-- Name: main_feedbackercandidate_feedbacker_id_c7b7f676; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_feedbackercandidate_feedbacker_id_c7b7f676 ON public.main_feedbackercandidate USING btree (feedbacker_id);


--
-- Name: main_feedbackrequest_area_id_7232ba2f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_feedbackrequest_area_id_7232ba2f ON public.main_feedbackrequest USING btree (area_id);


--
-- Name: main_feedbackrequest_feedbackee_id_74dece0f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_feedbackrequest_feedbackee_id_74dece0f ON public.main_feedbackrequest USING btree (feedbackee_id);


--
-- Name: main_feedbackrequest_feedbacker_id_10a6716c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_feedbackrequest_feedbacker_id_10a6716c ON public.main_feedbackrequest USING btree (feedbacker_id);


--
-- Name: main_purchase_feedback_id_ffc6b206; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_purchase_feedback_id_ffc6b206 ON public.main_purchase USING btree (feedback_id);


--
-- Name: main_purchase_feedbackee_id_885773db; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_purchase_feedbackee_id_885773db ON public.main_purchase USING btree (feedbackee_id);


--
-- Name: main_purchase_feedbacker_id_ff0da19c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_purchase_feedbacker_id_ff0da19c ON public.main_purchase USING btree (feedbacker_id);


--
-- Name: main_rating_feedbackee_id_4a68f4a0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_rating_feedbackee_id_4a68f4a0 ON public.main_rating USING btree (feedbackee_id);


--
-- Name: main_rating_feedbacker_id_d3cf720f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_rating_feedbacker_id_d3cf720f ON public.main_rating USING btree (feedbacker_id);


--
-- Name: main_tag_category_id_5edb617a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_tag_category_id_5edb617a ON public.main_tag USING btree (category_id);


--
-- Name: main_tag_feedback_id_d815f430; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_tag_feedback_id_d815f430 ON public.main_tag USING btree (feedback_id);


--
-- Name: users_specialism_category_id_36db4fdd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_specialism_category_id_36db4fdd ON public.users_specialism USING btree (category_id);


--
-- Name: users_specialism_feedbacker_id_651e2a94; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_specialism_feedbacker_id_651e2a94 ON public.users_specialism USING btree (feedbacker_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_feedbackercandidate main_feedbackercandi_feedback_id_8749740e_fk_main_feed; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackercandidate
    ADD CONSTRAINT main_feedbackercandi_feedback_id_8749740e_fk_main_feed FOREIGN KEY (feedback_id) REFERENCES public.main_feedbackrequest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_feedbackercandidate main_feedbackercandidate_feedbacker_id_c7b7f676_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackercandidate
    ADD CONSTRAINT main_feedbackercandidate_feedbacker_id_c7b7f676_fk_auth_user_id FOREIGN KEY (feedbacker_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_feedbackrequest main_feedbackrequest_area_id_7232ba2f_fk_main_area_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackrequest
    ADD CONSTRAINT main_feedbackrequest_area_id_7232ba2f_fk_main_area_id FOREIGN KEY (area_id) REFERENCES public.main_area(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_feedbackrequest main_feedbackrequest_feedbackee_id_74dece0f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackrequest
    ADD CONSTRAINT main_feedbackrequest_feedbackee_id_74dece0f_fk_auth_user_id FOREIGN KEY (feedbackee_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_feedbackrequest main_feedbackrequest_feedbacker_id_10a6716c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_feedbackrequest
    ADD CONSTRAINT main_feedbackrequest_feedbacker_id_10a6716c_fk_auth_user_id FOREIGN KEY (feedbacker_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_purchase main_purchase_feedback_id_ffc6b206_fk_main_feedbackrequest_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_purchase
    ADD CONSTRAINT main_purchase_feedback_id_ffc6b206_fk_main_feedbackrequest_id FOREIGN KEY (feedback_id) REFERENCES public.main_feedbackrequest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_purchase main_purchase_feedbackee_id_885773db_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_purchase
    ADD CONSTRAINT main_purchase_feedbackee_id_885773db_fk_auth_user_id FOREIGN KEY (feedbackee_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_purchase main_purchase_feedbacker_id_ff0da19c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_purchase
    ADD CONSTRAINT main_purchase_feedbacker_id_ff0da19c_fk_auth_user_id FOREIGN KEY (feedbacker_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_rating main_rating_feedbackee_id_4a68f4a0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_rating
    ADD CONSTRAINT main_rating_feedbackee_id_4a68f4a0_fk_auth_user_id FOREIGN KEY (feedbackee_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_rating main_rating_feedbacker_id_d3cf720f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_rating
    ADD CONSTRAINT main_rating_feedbacker_id_d3cf720f_fk_auth_user_id FOREIGN KEY (feedbacker_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_tag main_tag_category_id_5edb617a_fk_main_category_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tag
    ADD CONSTRAINT main_tag_category_id_5edb617a_fk_main_category_id FOREIGN KEY (category_id) REFERENCES public.main_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_tag main_tag_feedback_id_d815f430_fk_main_feedbackrequest_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tag
    ADD CONSTRAINT main_tag_feedback_id_d815f430_fk_main_feedbackrequest_id FOREIGN KEY (feedback_id) REFERENCES public.main_feedbackrequest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_specialism users_specialism_category_id_36db4fdd_fk_main_category_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_specialism
    ADD CONSTRAINT users_specialism_category_id_36db4fdd_fk_main_category_id FOREIGN KEY (category_id) REFERENCES public.main_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_specialism users_specialism_feedbacker_id_651e2a94_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_specialism
    ADD CONSTRAINT users_specialism_feedbacker_id_651e2a94_fk_auth_user_id FOREIGN KEY (feedbacker_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofile_user_id_87251ef1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_87251ef1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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

--
-- Name: UMRepo; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "UMRepo";


ALTER SCHEMA "UMRepo" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: AccessRequests; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo"."AccessRequests" (
    user_id integer NOT NULL,
    requested_at timestamp without time zone,
    status character varying(20) DEFAULT 'Pending'::character varying,
    request_id integer NOT NULL
);


ALTER TABLE "UMRepo"."AccessRequests" OWNER TO postgres;

--
-- Name: AccessRequests_request_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo"."AccessRequests_request_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo"."AccessRequests_request_id_seq" OWNER TO postgres;

--
-- Name: AccessRequests_request_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo"."AccessRequests_request_id_seq" OWNED BY "UMRepo"."AccessRequests".request_id;


--
-- Name: AccessRequests_user_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo"."AccessRequests_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo"."AccessRequests_user_id_seq" OWNER TO postgres;

--
-- Name: AccessRequests_user_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo"."AccessRequests_user_id_seq" OWNED BY "UMRepo"."AccessRequests".user_id;


--
-- Name: Attributes; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo"."Attributes" (
    name character varying(50),
    cat_id integer,
    input_type character varying(50),
    is_default boolean DEFAULT false,
    attr_id integer NOT NULL
);


ALTER TABLE "UMRepo"."Attributes" OWNER TO postgres;

--
-- Name: Attributes_attr_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo"."Attributes_attr_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo"."Attributes_attr_id_seq" OWNER TO postgres;

--
-- Name: Attributes_attr_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo"."Attributes_attr_id_seq" OWNED BY "UMRepo"."Attributes".attr_id;


--
-- Name: Category; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo"."Category" (
    cat_name character varying(100),
    cat_id integer NOT NULL
);


ALTER TABLE "UMRepo"."Category" OWNER TO postgres;

--
-- Name: Category_cat_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo"."Category_cat_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo"."Category_cat_id_seq" OWNER TO postgres;

--
-- Name: Category_cat_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo"."Category_cat_id_seq" OWNED BY "UMRepo"."Category".cat_id;


--
-- Name: User; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo"."User" (
    "Name" character varying(50),
    "Surname" character varying(50),
    email character varying(100),
    "Pass_Hash" text,
    "Status" character varying(20),
    user_id integer NOT NULL,
    "RoleID" integer
);


ALTER TABLE "UMRepo"."User" OWNER TO postgres;

--
-- Name: User_user_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo"."User_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo"."User_user_id_seq" OWNER TO postgres;

--
-- Name: User_user_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo"."User_user_id_seq" OWNED BY "UMRepo"."User".user_id;


--
-- Name: file; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo".file (
    name character varying(100) NOT NULL,
    description text,
    path text NOT NULL,
    uploader integer,
    upload_date timestamp without time zone,
    visibility character varying(20) DEFAULT 'OPEN'::character varying,
    cat_id integer,
    file_id integer NOT NULL,
    subject_category character varying(20)
);


ALTER TABLE "UMRepo".file OWNER TO postgres;

--
-- Name: file_attributes; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo".file_attributes (
    fid integer NOT NULL,
    file_id integer,
    attr_id integer,
    value text
);


ALTER TABLE "UMRepo".file_attributes OWNER TO postgres;

--
-- Name: file_file_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo".file_file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo".file_file_id_seq OWNER TO postgres;

--
-- Name: file_file_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo".file_file_id_seq OWNED BY "UMRepo".file.file_id;


--
-- Name: pending; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo".pending (
    "Name" character varying(50),
    "Surname" character varying(50),
    email character varying(100),
    "Pass_Hash" text,
    "Status" character varying(20),
    "RoleID" integer,
    user_id integer NOT NULL
);


ALTER TABLE "UMRepo".pending OWNER TO postgres;

--
-- Name: pending_user_id_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo".pending_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo".pending_user_id_seq OWNER TO postgres;

--
-- Name: pending_user_id_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo".pending_user_id_seq OWNED BY "UMRepo".pending.user_id;


--
-- Name: roles; Type: TABLE; Schema: UMRepo; Owner: postgres
--

CREATE TABLE "UMRepo".roles (
    "RoleName" character varying(50),
    status character varying(20),
    "RoleID" integer NOT NULL
);


ALTER TABLE "UMRepo".roles OWNER TO postgres;

--
-- Name: roles_RoleID_seq; Type: SEQUENCE; Schema: UMRepo; Owner: postgres
--

CREATE SEQUENCE "UMRepo"."roles_RoleID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "UMRepo"."roles_RoleID_seq" OWNER TO postgres;

--
-- Name: roles_RoleID_seq; Type: SEQUENCE OWNED BY; Schema: UMRepo; Owner: postgres
--

ALTER SEQUENCE "UMRepo"."roles_RoleID_seq" OWNED BY "UMRepo".roles."RoleID";


--
-- Name: AccessRequests user_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."AccessRequests" ALTER COLUMN user_id SET DEFAULT nextval('"UMRepo"."AccessRequests_user_id_seq"'::regclass);


--
-- Name: AccessRequests request_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."AccessRequests" ALTER COLUMN request_id SET DEFAULT nextval('"UMRepo"."AccessRequests_request_id_seq"'::regclass);


--
-- Name: Attributes attr_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."Attributes" ALTER COLUMN attr_id SET DEFAULT nextval('"UMRepo"."Attributes_attr_id_seq"'::regclass);


--
-- Name: Category cat_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."Category" ALTER COLUMN cat_id SET DEFAULT nextval('"UMRepo"."Category_cat_id_seq"'::regclass);


--
-- Name: User user_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."User" ALTER COLUMN user_id SET DEFAULT nextval('"UMRepo"."User_user_id_seq"'::regclass);


--
-- Name: file file_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".file ALTER COLUMN file_id SET DEFAULT nextval('"UMRepo".file_file_id_seq'::regclass);


--
-- Name: pending user_id; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".pending ALTER COLUMN user_id SET DEFAULT nextval('"UMRepo".pending_user_id_seq'::regclass);


--
-- Name: roles RoleID; Type: DEFAULT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".roles ALTER COLUMN "RoleID" SET DEFAULT nextval('"UMRepo"."roles_RoleID_seq"'::regclass);


--
-- Data for Name: AccessRequests; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo"."AccessRequests" (user_id, requested_at, status, request_id) FROM stdin;
\.


--
-- Data for Name: Attributes; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo"."Attributes" (name, cat_id, input_type, is_default, attr_id) FROM stdin;
Semester	1	integer	f	1
Year	1	integer	f	2
Course Name	1	character varying (50)	f	3
Lecturer Name	1	character varying (50)	f	4
Topic	1	character varying (50)	f	5
Assignment number	2	integer	f	6
Due Date	2	timestamp without timezone	f	7
Year	2	integer	f	8
Course Name	2	character varying (50)	f	9
Instructor Name	2	character varying (50)	f	10
Experiment Title	5	character varying (50)	f	11
Subject	5	character varying (50)	f	12
Instructor	5	character varying (50)	f	13
Date Conducted	5	date without timezone	f	14
Lab Partners	5	character varying (50)	f	15
Title	6	character varying (50)	f	16
Student Name	6	character varying (50)	f	17
Supervisor	6	character varying (50)	f	18
Department	6	date without timezone	f	19
Year	6	character varying (50)	f	20
Abstract	6	character varying (100)	f	21
Degree Level	6	character varying (50)	f	22
Title	8	character varying (50)	f	28
Speaker Name	8	character varying (50)	f	29
Event Name or Course	8	character varying (50)	f	30
Date Presented	8	date without timezone	f	31
Topic	8	character varying (50)	f	32
Title	7	character varying (50)	f	37
Title	4	character varying (50)	f	39
Authors	4	character varying (50)	f	40
Publication Year	4	integer	f	41
Journal/Conference Name	4	character varying (50)	f	42
Course Name	3	character varying (50)	f	23
Exam Type	3	character varying (50)	f	24
Year	3	integer	f	25
Instructor	3	character varying (50)	f	26
Duration	3	Duration	f	27
Course Name	7	character varying (50)	f	33
Instructor/Presenter	7	character varying (50)	f	34
Duration	7	integer	f	35
Topic	7	character varying (50)	f	36
\.


--
-- Data for Name: Category; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo"."Category" (cat_name, cat_id) FROM stdin;
Lecture Notes	1
Assignment	2
Exam/Solution	3
Research Paper	4
Lab Report	5
Thesis/Dissertation	6
Video	7
Presentation	8
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo"."User" ("Name", "Surname", email, "Pass_Hash", "Status", user_id, "RoleID") FROM stdin;
Mario	Mario	spmario64@nintendo.com	$2b$12$2hOXGAtmNvPmhjChQjoTzOuBsEwOq9nlOcZ32PIkFFAfJmJtiHnNu	\N	5	\N
Keith	Schembri	k8schem@gmail.com	$2b$12$xR.kTmBdP.JpLCxiGIMuTOLulRnlcw2dPXdQVeqJMqDdTZMr9gbCy	Teacher	2	3
Naomi	Schembri	naomi@pornhub.23.com	$2b$12$PpfLGQZvkNsWyGWdj48tjeMLIf9EvadYP7cgwhleJz9BE4bjQUIuS	\N	6	\N
Keetus	Deleetus	kdel77@email.com	$2b$12$ZL2q7MT9JjfUAt//e9qUq.rIwFa31iV6PdbaoYpDOx.xNQYCl3rae	\N	7	1
\.


--
-- Data for Name: file; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo".file (name, description, path, uploader, upload_date, visibility, cat_id, file_id, subject_category) FROM stdin;
banana	dafs	c:\\Users\\k8sch\\Documents\\GAPT_Library\\web\\uploads\\parser.py	2	2025-04-22 00:00:00	Open Access	2	17	Humanities
banana	hello	C:\\Users\\k8sch\\Documents\\GAPT_Library\\web\\uploads\\eafb0a96-5ffc-4916-88d0-b2a60766fa5f.png	2	2025-04-29 00:00:00	Restricted	4	18	Biology
\.


--
-- Data for Name: file_attributes; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo".file_attributes (fid, file_id, attr_id, value) FROM stdin;
\.


--
-- Data for Name: pending; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo".pending ("Name", "Surname", email, "Pass_Hash", "Status", "RoleID", user_id) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: UMRepo; Owner: postgres
--

COPY "UMRepo".roles ("RoleName", status, "RoleID") FROM stdin;
Student	Set	1
Teacher	Set	2
Librarian	Set	3
\.


--
-- Name: AccessRequests_request_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo"."AccessRequests_request_id_seq"', 2, true);


--
-- Name: AccessRequests_user_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo"."AccessRequests_user_id_seq"', 1, false);


--
-- Name: Attributes_attr_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo"."Attributes_attr_id_seq"', 42, true);


--
-- Name: Category_cat_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo"."Category_cat_id_seq"', 8, true);


--
-- Name: User_user_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo"."User_user_id_seq"', 7, true);


--
-- Name: file_file_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo".file_file_id_seq', 18, true);


--
-- Name: pending_user_id_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo".pending_user_id_seq', 8, true);


--
-- Name: roles_RoleID_seq; Type: SEQUENCE SET; Schema: UMRepo; Owner: postgres
--

SELECT pg_catalog.setval('"UMRepo"."roles_RoleID_seq"', 3, true);


--
-- Name: AccessRequests AccessRequests_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."AccessRequests"
    ADD CONSTRAINT "AccessRequests_pkey" PRIMARY KEY (request_id);


--
-- Name: Attributes Attributes_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."Attributes"
    ADD CONSTRAINT "Attributes_pkey" PRIMARY KEY (attr_id);


--
-- Name: Category Category_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."Category"
    ADD CONSTRAINT "Category_pkey" PRIMARY KEY (cat_id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);


--
-- Name: file_attributes file_attributes_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".file_attributes
    ADD CONSTRAINT file_attributes_pkey PRIMARY KEY (fid);


--
-- Name: file file_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".file
    ADD CONSTRAINT file_pkey PRIMARY KEY (file_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY ("RoleID");


--
-- Name: file fk_cats; Type: FK CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".file
    ADD CONSTRAINT fk_cats FOREIGN KEY (cat_id) REFERENCES "UMRepo"."Category"(cat_id);


--
-- Name: Attributes fk_cats; Type: FK CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."Attributes"
    ADD CONSTRAINT fk_cats FOREIGN KEY (cat_id) REFERENCES "UMRepo"."Category"(cat_id);


--
-- Name: file_attributes fk_file_attributes; Type: FK CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".file_attributes
    ADD CONSTRAINT fk_file_attributes FOREIGN KEY (file_id) REFERENCES "UMRepo".file(file_id);


--
-- Name: file fk_file_uploader; Type: FK CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo".file
    ADD CONSTRAINT fk_file_uploader FOREIGN KEY (uploader) REFERENCES "UMRepo"."User"(user_id);


--
-- Name: User fk_role; Type: FK CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."User"
    ADD CONSTRAINT fk_role FOREIGN KEY ("RoleID") REFERENCES "UMRepo".roles("RoleID");


--
-- Name: AccessRequests fk_useraccess; Type: FK CONSTRAINT; Schema: UMRepo; Owner: postgres
--

ALTER TABLE ONLY "UMRepo"."AccessRequests"
    ADD CONSTRAINT fk_useraccess FOREIGN KEY (user_id) REFERENCES "UMRepo"."User"(user_id);


--
-- PostgreSQL database dump complete
--


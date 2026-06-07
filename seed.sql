--
-- PostgreSQL database dump
--

\restrict u2Pq2Ra08uJ0NkRfWtfjefJWTavlwUm3GgsqyPa5hrN98SGXP9Fs9YbH6Pqgm9d

-- Dumped from database version 16.13 (Homebrew)
-- Dumped by pg_dump version 16.13 (Homebrew)

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
-- Name: co2_data; Type: TABLE; Schema: public; Owner: zara
--

CREATE TABLE public.co2_data (
    id integer NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    co2_g_per_kwh double precision,
    co2_kg_per_kwh double precision
);


ALTER TABLE public.co2_data OWNER TO zara;

--
-- Name: co2_data_id_seq; Type: SEQUENCE; Schema: public; Owner: zara
--

CREATE SEQUENCE public.co2_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.co2_data_id_seq OWNER TO zara;

--
-- Name: co2_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zara
--

ALTER SEQUENCE public.co2_data_id_seq OWNED BY public.co2_data.id;


--
-- Name: decisions; Type: TABLE; Schema: public; Owner: zara
--

CREATE TABLE public.decisions (
    id integer NOT NULL,
    "timestamp" timestamp with time zone,
    action text,
    reward double precision
);


ALTER TABLE public.decisions OWNER TO zara;

--
-- Name: decisions_id_seq; Type: SEQUENCE; Schema: public; Owner: zara
--

CREATE SEQUENCE public.decisions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.decisions_id_seq OWNER TO zara;

--
-- Name: decisions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zara
--

ALTER SEQUENCE public.decisions_id_seq OWNED BY public.decisions.id;


--
-- Name: predictions; Type: TABLE; Schema: public; Owner: zara
--

CREATE TABLE public.predictions (
    id integer NOT NULL,
    "timestamp" timestamp with time zone,
    predicted_co2 double precision
);


ALTER TABLE public.predictions OWNER TO zara;

--
-- Name: predictions_id_seq; Type: SEQUENCE; Schema: public; Owner: zara
--

CREATE SEQUENCE public.predictions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.predictions_id_seq OWNER TO zara;

--
-- Name: predictions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zara
--

ALTER SEQUENCE public.predictions_id_seq OWNED BY public.predictions.id;


--
-- Name: weather_data; Type: TABLE; Schema: public; Owner: zara
--

CREATE TABLE public.weather_data (
    id integer NOT NULL,
    "timestamp" timestamp without time zone,
    temperature double precision,
    humidity double precision,
    wind_speed double precision,
    solar_radiation double precision
);


ALTER TABLE public.weather_data OWNER TO zara;

--
-- Name: weather_data_id_seq; Type: SEQUENCE; Schema: public; Owner: zara
--

CREATE SEQUENCE public.weather_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weather_data_id_seq OWNER TO zara;

--
-- Name: weather_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zara
--

ALTER SEQUENCE public.weather_data_id_seq OWNED BY public.weather_data.id;


--
-- Name: co2_data id; Type: DEFAULT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.co2_data ALTER COLUMN id SET DEFAULT nextval('public.co2_data_id_seq'::regclass);


--
-- Name: decisions id; Type: DEFAULT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.decisions ALTER COLUMN id SET DEFAULT nextval('public.decisions_id_seq'::regclass);


--
-- Name: predictions id; Type: DEFAULT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.predictions ALTER COLUMN id SET DEFAULT nextval('public.predictions_id_seq'::regclass);


--
-- Name: weather_data id; Type: DEFAULT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.weather_data ALTER COLUMN id SET DEFAULT nextval('public.weather_data_id_seq'::regclass);


--
-- Data for Name: co2_data; Type: TABLE DATA; Schema: public; Owner: zara
--

COPY public.co2_data (id, "timestamp", co2_g_per_kwh, co2_kg_per_kwh) FROM stdin;
1	2026-04-13 09:40:26.787469+10	120.5	0.1205
2	2026-04-13 09:53:14.811403+10	905.7942176	0.9057942
3	2026-04-13 09:53:15.81732+10	977.153454	0.9771535
4	2026-04-13 09:53:16.817738+10	1022.039242	1.0220392
5	2026-04-13 09:53:17.829902+10	1047.364364	1.0473644
6	2026-04-13 09:53:18.830719+10	1067.552372	1.0675524
7	2026-04-13 09:53:19.831997+10	1083.575837	1.0835758
8	2026-04-13 09:53:20.83662+10	1027.684596	1.0276846
9	2026-04-13 09:53:21.842961+10	924.7375867	0.9247376
10	2026-04-13 09:53:22.848812+10	750.0600665	0.7500601
11	2026-04-13 09:53:23.854823+10	648.4439711	0.648444
12	2026-04-13 09:53:24.860381+10	661.3996234	0.6613996
13	2026-04-13 09:53:25.860749+10	748.7196906	0.7487197
14	2026-04-13 09:53:26.86392+10	755.2343541	0.7552344
15	2026-04-13 09:53:27.868875+10	746.6512074	0.7466512
16	2026-04-13 09:53:28.875047+10	742.6284037	0.7426284
17	2026-04-13 09:53:29.881167+10	684.5038109	0.6845038
18	2026-04-13 09:53:30.883653+10	688.1668883	0.6881669
19	2026-04-13 09:53:31.888979+10	670.8112367	0.6708112
20	2026-04-13 09:53:32.889894+10	758.131331	0.7581313
21	2026-04-13 09:53:33.894894+10	787.1246654	0.7871247
22	2026-04-13 09:53:34.895544+10	781.6936494	0.7816936
23	2026-04-13 09:53:35.896911+10	809.1114084	0.8091114
24	2026-04-13 09:53:36.902272+10	830.3317836	0.8303318
25	2026-04-13 09:53:37.904032+10	853.6369161	0.8536369
26	2026-04-13 09:53:38.910696+10	899.9571186	0.8999571
27	2026-04-13 09:53:39.91581+10	924.8209542	0.924821
28	2026-04-13 09:53:40.922015+10	939.9347032	0.9399347
29	2026-04-13 09:53:41.925804+10	941.2295126	0.9412295
30	2026-04-13 09:53:42.926021+10	933.5005652	0.9335006
31	2026-04-13 09:53:43.928104+10	936.244978	0.936245
32	2026-04-13 09:53:44.932652+10	929.6252118	0.9296252
33	2026-04-13 09:53:45.938367+10	889.6735025	0.8896735
34	2026-04-13 09:53:46.9402+10	836.6922091	0.8366922
35	2026-04-13 09:53:47.943575+10	743.8280472	0.743828
36	2026-04-13 09:53:48.944813+10	680.3204161	0.6803204
37	2026-04-13 09:53:49.950642+10	617.8215227	0.6178215
38	2026-04-13 09:53:50.955647+10	599.4084113	0.5994084
39	2026-04-13 09:53:51.959678+10	526.9272536	0.5269273
40	2026-04-13 09:53:52.960607+10	544.3441385	0.5443441
\.


--
-- Data for Name: decisions; Type: TABLE DATA; Schema: public; Owner: zara
--

COPY public.decisions (id, "timestamp", action, reward) FROM stdin;
\.


--
-- Data for Name: predictions; Type: TABLE DATA; Schema: public; Owner: zara
--

COPY public.predictions (id, "timestamp", predicted_co2) FROM stdin;
\.


--
-- Data for Name: weather_data; Type: TABLE DATA; Schema: public; Owner: zara
--

COPY public.weather_data (id, "timestamp", temperature, humidity, wind_speed, solar_radiation) FROM stdin;
1	2024-01-01 03:00:00	12.78	92.38	2.19	0
2	2024-01-01 04:00:00	12.63	92.41	1.99	0
3	2024-01-01 05:00:00	13.26	89.88	1.96	31.38
4	2024-01-01 06:00:00	15.13	79.64	2.11	183.48
5	2024-01-01 07:00:00	16.62	73.17	1.41	353.88
6	2024-01-01 08:00:00	18.77	66.04	0.26	536.12
7	2024-01-01 09:00:00	20.75	61.67	0.78	815.5
8	2024-01-01 10:00:00	22.41	58.36	1.33	953.55
9	2024-01-01 16:00:00	21.4	66.36	4.95	496.73
10	2024-01-01 17:00:00	19.88	71.73	5.03	321.83
11	2024-01-01 18:00:00	18.16	78.43	4.79	140.93
12	2024-01-01 19:00:00	16.79	83.97	4.11	16.35
13	2024-01-01 20:00:00	16.15	86.78	3.54	0
14	2024-01-01 21:00:00	15.96	88.33	3.23	0
15	2024-01-01 22:00:00	15.85	90.03	3.14	0
16	2024-01-01 23:00:00	15.78	91.9	2.82	0
17	2024-01-02 00:00:00	15.74	93.4	2.29	0
18	2024-01-02 01:00:00	15.68	94.91	2.17	0
19	2024-01-02 02:00:00	15.56	96.68	2.08	0
20	2024-01-02 03:00:00	15.58	97.48	2	0
21	2024-01-02 04:00:00	15.48	98.71	1.76	0
22	2024-01-02 05:00:00	15.94	96.66	1.51	27.05
23	2024-01-02 06:00:00	17.18	89.85	1.38	168.7
24	2024-01-02 07:00:00	18.55	83.27	0.91	341.83
25	2024-01-02 08:00:00	20.47	75.88	0.62	527.88
26	2024-01-02 09:00:00	22.74	68.16	0.31	698.67
27	2024-01-02 10:00:00	24.98	62.05	0.41	816.17
28	2024-01-02 11:00:00	26.4	57.88	1.06	644.45
29	2024-01-02 12:00:00	27.04	56.39	1.66	103.85
30	2024-01-02 13:00:00	27.41	55.77	1.22	40.75
31	2024-01-02 14:00:00	26.22	60.59	1.77	38.28
32	2024-01-02 15:00:00	25.21	66.51	1.89	26.62
33	2024-01-02 16:00:00	24.42	72.18	1.79	23
34	2024-01-02 17:00:00	23.53	77.19	1.88	112.4
35	2024-01-02 18:00:00	22.54	82.84	2.16	53.33
36	2024-01-02 19:00:00	21.62	88.59	1.36	10.9
37	2024-01-02 20:00:00	21.32	91.44	1.46	0
38	2024-01-02 21:00:00	20.93	93.79	1.58	0
39	2024-01-02 22:00:00	20.43	95.91	1.27	0
40	2024-01-02 23:00:00	20	96.76	0.99	0
\.


--
-- Name: co2_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zara
--

SELECT pg_catalog.setval('public.co2_data_id_seq', 40, true);


--
-- Name: decisions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zara
--

SELECT pg_catalog.setval('public.decisions_id_seq', 1, false);


--
-- Name: predictions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zara
--

SELECT pg_catalog.setval('public.predictions_id_seq', 1, false);


--
-- Name: weather_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zara
--

SELECT pg_catalog.setval('public.weather_data_id_seq', 40, true);


--
-- Name: co2_data co2_data_pkey; Type: CONSTRAINT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.co2_data
    ADD CONSTRAINT co2_data_pkey PRIMARY KEY (id);


--
-- Name: decisions decisions_pkey; Type: CONSTRAINT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.decisions
    ADD CONSTRAINT decisions_pkey PRIMARY KEY (id);


--
-- Name: predictions predictions_pkey; Type: CONSTRAINT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.predictions
    ADD CONSTRAINT predictions_pkey PRIMARY KEY (id);


--
-- Name: weather_data weather_data_pkey; Type: CONSTRAINT; Schema: public; Owner: zara
--

ALTER TABLE ONLY public.weather_data
    ADD CONSTRAINT weather_data_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict u2Pq2Ra08uJ0NkRfWtfjefJWTavlwUm3GgsqyPa5hrN98SGXP9Fs9YbH6Pqgm9d


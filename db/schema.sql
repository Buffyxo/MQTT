--
-- PostgreSQL database dump
--

\restrict xCisrSVoG0ofN82MJr3AgJYWzuRZ49Fyy9482XeBparx7FUzazgOwIuUBPzfmZr

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
-- PostgreSQL database dump complete
--

\unrestrict xCisrSVoG0ofN82MJr3AgJYWzuRZ49Fyy9482XeBparx7FUzazgOwIuUBPzfmZr


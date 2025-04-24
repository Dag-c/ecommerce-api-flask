--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
--SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roleenum AS ENUM (
    'buyer',
    'seller',
    'admin'
);


ALTER TYPE public.roleenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    id integer NOT NULL,
    order_id integer,
    product_id integer,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL,
    CONSTRAINT order_items_price_check CHECK ((price > (0)::numeric)),
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0))
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.order_items_id_seq OWNER TO postgres;

--
-- Name: order_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    buyer_id integer,
    total numeric(10,2) NOT NULL,
    status character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'shipped'::character varying, 'delivered'::character varying, 'canceled'::character varying])::text[]))),
    CONSTRAINT orders_total_check CHECK ((total > (0)::numeric))
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    seller_id integer,
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2) NOT NULL,
    stock integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT products_price_check CHECK ((price > (0)::numeric)),
    CONSTRAINT products_stock_check CHECK ((stock >= 0))
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password text NOT NULL,
    role character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['buyer'::character varying, 'seller'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: order_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (id, order_id, product_id, quantity, price) FROM stdin;
1	12	2	5	1351.00
2	12	2	2	1351.00
5	14	2	1	1351.00
6	14	2	1	1351.00
7	15	2	2	1351.00
8	15	2	1	1351.00
9	15	2	3	1351.00
10	16	2	1	1351.00
11	16	2	2	1351.00
12	16	2	3	1351.00
13	17	2	2	1351.00
14	17	2	3	1351.00
15	17	2	4	1351.00
16	18	2	3	1351.00
17	18	2	5	1351.00
18	18	2	4	1351.00
19	19	2	1	1351.00
20	19	2	1	1351.00
21	19	2	1	1351.00
22	20	2	6	1350.50
23	20	2	3	1350.50
24	20	2	7	1350.50
25	21	2	1	1350.50
26	21	2	1	1350.50
27	21	2	1	1350.50
28	22	2	1	1350.50
29	22	2	1	1350.50
30	22	2	1	1350.50
31	23	2	1	1350.50
32	23	2	1	1350.50
33	23	2	1	1350.50
34	24	2	1	1350.50
35	24	2	1	1350.50
36	24	2	1	1350.50
37	25	2	1	1350.50
38	25	2	1	1350.50
39	25	2	1	1350.50
40	26	2	1	1350.50
41	26	2	1	1350.50
42	26	2	1	1350.50
43	27	2	1	1350.50
44	27	2	1	1350.50
45	27	2	1	1350.50
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, buyer_id, total, status, created_at) FROM stdin;
12	4	9453.50	pending	2025-03-18 13:56:07.857073
18	4	16206.00	pending	2025-03-18 16:05:11.38218
19	4	4051.50	pending	2025-03-18 16:10:41.128946
20	4	21608.00	pending	2025-03-18 16:16:12.967677
14	4	3000.47	shipped	2025-03-18 14:15:52.983156
15	4	8542.18	shipped	2025-03-18 14:17:19.242052
16	4	8325.52	shipped	2025-03-18 14:23:59.137929
17	4	12437.13	shipped	2025-03-18 16:02:59.052988
21	6	4051.50	pending	2025-03-22 16:13:48.856811
22	6	4051.50	pending	2025-03-22 16:15:26.144576
23	6	4051.50	pending	2025-03-22 16:16:05.323958
24	6	4051.50	pending	2025-03-22 16:18:25.752365
25	6	4051.50	pending	2025-03-22 16:20:14.049843
26	6	4051.50	pending	2025-03-22 16:21:23.681392
27	6	4051.50	pending	2025-03-22 16:26:21.036032
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, seller_id, name, description, price, stock, created_at) FROM stdin;
2	5	Pantalones skiny Levi's	Jeans 32x36 cafe primavera 2025	1350.50	7	2025-03-17 13:42:55.702363
3	6	smartphone	Xiaomi 13T Plus 250GB octa-core	1255.85	35	2025-04-03 20:01:10.206963
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role, created_at) FROM stdin;
1	Juan P‚rez	juan@example.com	12345	seller	2025-03-15 16:15:48.099446
5	Armando Cruz	Armando@example.com	w3f4t5	seller	2025-03-16 17:52:38.785254
4	Diego Guillen	Crusito@example.com	A1B2c3	seller	2025-03-16 17:28:23.186884
6	Jose Perez	Pepe_23@example.com	$2b$12$x4N8g3kA4GtiIE4kmeFWGe4KSFFFvc5WHlzA7.Is1s74yOj6qi7iK	seller	2025-03-22 11:09:50.72451
7	John Doe	john.doe@example.com	$2b$12$c013zpbkFkhzT8iZMEFbS.GvMrUx2HvogWcFW90hliiN5VkHAmaK6	buyer	2025-03-24 13:29:25.364385
9	Developer	example.1@example.com	$2b$12$NMOLyBCWUmRsNBoritgi4Oz5OxW9Olb2FNyr/SL/IKZ6aTZ1TonQq	admin	2025-04-03 19:53:30.237559
\.


--
-- Name: order_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.order_items_id_seq', 45, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 27, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: orders orders_buyer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: products products_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


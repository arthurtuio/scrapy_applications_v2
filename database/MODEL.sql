CREATE TABLE scrapy.credentials_paroquia (
	id bigserial NOT NULL,
	unidade_consumidora text NOT NULL,
	tipo_documento text NOT NULL,
	numero_documento text NOT NULL,
	tipo_usuario text NOT NULL,
	password_value text NOT NULL,
	mesInicial text NOT NULL,
	anoInicial text NOT NULL,
	mesFinal text NOT NULL,
	anoFinal text NOT NULL,
	sync_status text NOT null default false,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now()
);


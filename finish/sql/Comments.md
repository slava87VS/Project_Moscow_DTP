1. Кажется есть смысл указывать индексы для часто используемых столбцов. На твоих объёмах конечно никак не повлияет, но в случае значительного увеличения объёма может сильно помочь, лучше смотреть в будущее )

```sql
CREATE INDEX idx_properties_id ON dds_1.moscow_dtp_dim (properties_id);
CREATE INDEX idx_properties_region ON dds_1.moscow_dtp_dim (properties_region);
```

2. А добрая половина столбцов может иметь нуллы? Кажется лучше прописать `NOT NULL`

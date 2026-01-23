# ✅ NEW: JSON metadata dump
def export_metadata_to_json(self, metadata_list, output_path):
json_data = []

for m in metadata_list:
    json_data.append({
        "file_name": m.name,
        "absolute_path": str(m.path),
        "extension": m.extension,
        "file_type": m.file_type,
        "size_bytes": m.size_bytes,
        "size_kb": round(m.size_bytes / 1024, 2),
        "size_mb": round(m.size_bytes / (1024**2), 2),
        "created_at": m.created_at.isoformat(),
        "modified_at": m.modified_at.isoformat(),
        "hash_value": m.hash_value
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)

print(f"\n📄 Metadata JSON saved to: {output_path}")
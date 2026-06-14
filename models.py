from dataclasses import dataclass
from datetime import datetime
from database import get_connection


@dataclass
class Instance:
    id: int | None
    name: str
    instance_type: str
    state: str
    created_at: str

    @staticmethod
    def all():
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, instance_type, state, created_at FROM instances")
        rows = c.fetchall()
        conn.close()
        return [Instance(*row) for row in rows]

    @staticmethod
    def get(instance_id: int):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "SELECT id, name, instance_type, state, created_at FROM instances WHERE id = ?",
            (instance_id,),
        )
        row = c.fetchone()
        conn.close()
        return Instance(*row) if row else None

    @staticmethod
    def create(name: str, instance_type: str):
        conn = get_connection()
        c = conn.cursor()
        created_at = datetime.utcnow().isoformat()
        state = "stopped"
        c.execute(
            "INSERT INTO instances (name, instance_type, state, created_at) VALUES (?, ?, ?, ?)",
            (name, instance_type, state, created_at),
        )
        conn.commit()
        instance_id = c.lastrowid
        conn.close()
        return Instance.get(instance_id)

    def update_state(self, new_state: str):
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE instances SET state = ? WHERE id = ?",
            (new_state, self.id),
        )
        conn.commit()
        conn.close()
        self.state = new_state

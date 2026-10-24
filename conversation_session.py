class ConversationSession:
    def __init__(self) -> None:
        self.previous_interaction_id: str | None = None

    def update(self, interaction_id: str) -> None:
        self.previous_interaction_id = interaction_id
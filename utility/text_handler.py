
class Text_Handler:
    @staticmethod
    def truncate_text(text: str, max_length: int = 50) -> str:
        """
        Truncate text to a maximum length and add ellipsis if needed.
        
        Args:
            text (str): Text to truncate
            max_length (int): Maximum length before truncation
        
        Returns:
            str: Truncated text with ellipsis if needed
        """
        text = str(text)
        if len(text) > max_length:
            return text[:max_length -3] + '...'
        return text
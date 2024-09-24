"""
This file contains the utility functions for preprocessing text data
"""
import re
from urllib.parse import urlparse

import emoji


class TextPreProcessors:
    @staticmethod
    def remove_emoji(text: str) -> str:
        return emoji.replace_emoji(text, "")

    @staticmethod
    def transform_emoji_into_characters(text: str) -> str:
        return emoji.demojize(text, delimiters=('', ''))

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def case_folding(text: str) -> str:
        return text.casefold()

    @staticmethod
    def remove_hyperlinks(text: str) -> str:
        """
        Remove hyperlinks from the text
        """

        def _extract_meaningful_data(match):
            url = match.group()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url  # Adding a default protocol if not present
            parsed_url = urlparse(url)

            if parsed_url.hostname:
                domain_parts = parsed_url.hostname.split('.')
                return domain_parts[-2] if len(domain_parts) >= 2 else parsed_url.hostname
            else:
                return url

        return re.sub(r'(https?://)?\S+', _extract_meaningful_data, text)

    @staticmethod
    def remove_tags(text: str) -> str:
        """
        Remove tags from the text
        """
        return re.sub(r'<.*?>', ' ', text)

    @staticmethod
    def remove_non_alpha_numeric_characters(text: str) -> str:
        """
        Remove non-alphabetic characters from the text
        """
        return re.sub(r'[^A-Za-z0-9\s]+', '', text)

    @staticmethod
    def remove_stopwords(text: str) -> str:
        """
        Remove stopwords from the text
        """
        stopwords = ['is', 'a']
        tokens = text.split()
        clean_tokens = [t for t in tokens if not t in stopwords]
        return " ".join(clean_tokens)

    @staticmethod
    def remove_short_tokens(text: str, min_length: int = 1) -> str:
        """
        Remove tokens with length less than min_length
        """
        tokens = text.split()
        clean_tokens = [t for t in tokens if len(t) > min_length]
        return " ".join(clean_tokens)

    @staticmethod
    def remove_repeated_characters(text: str) -> str:
        """
        Remove repeated characters from the text
        """
        return re.sub(r'(.)\1+', r'\1', text)


def _module_testing():
    test_text = 'Hi 🤔 How is your 🙈 and 😌. Have a nice weekend 💕👭👙. Go visit www.naughtyindia.com'
    print(TextPreProcessors.remove_emoji(test_text))


if __name__ == '__main__':
    _module_testing()

from typing import List

from backend.preprocessors.text import TextPreProcessors
from backend.recall.plugins.searchquerygenerator.interface import BaseSearchQueryGenerator


class Cpu(BaseSearchQueryGenerator):
    _LEMMAS_TO_REMOVE = {'why', 'what', 'how', 'who', 'where', 'when', 'which', 'is', 'are'}

    def generate(self, user_query: str) -> List[str]:
        pre_processor = TextPreProcessors()
        user_query = pre_processor.remove_extra_spaces(user_query)
        user_query = pre_processor.case_folding(user_query)
        user_query = pre_processor.transform_emoji_into_characters(user_query)
        user_query = pre_processor.remove_extra_spaces(user_query)
        user_query = pre_processor.remove_hyperlinks(user_query)
        user_query = pre_processor.remove_tags(user_query)
        user_query = pre_processor.remove_non_alpha_numeric_characters(user_query)
        user_query = self.remove_lemmas(user_query)
        return [user_query]

    @staticmethod
    def remove_lemmas(user_query) -> str:
        filtered_text = ' '.join([word for word in user_query.split() if word.lower() not in Cpu._LEMMAS_TO_REMOVE])
        return filtered_text


def _module_testing():
    cpu = Cpu()
    print(cpu.generate('Who is the president of America?'))


if __name__ == '__main__':
    _module_testing()

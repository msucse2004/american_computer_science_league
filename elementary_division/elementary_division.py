from american_computer_science_league import AmericanComputerScienceLeague


class ElementaryDivision(AmericanComputerScienceLeague):
    _registry = {}

    @classmethod
    def register_child(cls, class_name, class_instance):
        cls._registry[class_name] = class_instance

    def __init__(self):
        super().__init__()
        self.child_classes = self._registry
        self.child_list = list(self.child_classes.keys())
        pass

    """
    # 부모 클래스에서 자식 인스턴스를 얻는 메서드
    def get_problem_answer_instance(self, chapter_name):
        chapter_class = self.chapter_classes.get(chapter_name)
        if chapter_class:
            return chapter_class()  # 클래스를 인스턴스화하여 반환
        return None
    """
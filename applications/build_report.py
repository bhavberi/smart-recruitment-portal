from abc import ABC, abstractmethod
from models.applications import Report

class AbstractReportBuilder(ABC):
    """
    Abstract class for building reports
    """
    
    @property
    @abstractmethod
    def report(self) -> None:
        pass

    @abstractmethod
    def build_user(self, user: str) -> None:
        pass

    @abstractmethod
    def build_llama(self, llama: str) -> None:
        pass

    @abstractmethod
    def build_mbti(self, mbti: str) -> None:
        pass

    @abstractmethod
    def build_report_gen(self, report_gen: str) -> None:
        pass

    @abstractmethod
    def build_sentiment(self, sentiment: str) -> None:
        pass

class FullReportBuilder(AbstractReportBuilder):
    """
    Concrete class for building full reports
    """
    
    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self._report = Report()

    @property
    def report(self) -> Report:
        report = self._report
        self.reset()
        return report

    def build_user(self, user: str) -> None:
        self._report.user = user

    def build_llama(self, llama: str) -> None:
        self._report.llama = llama

    def build_mbti(self, mbti: str) -> None:
        self._report.mbti = mbti

    def build_report_gen(self, report_gen: str) -> None:
        self._report.report_gen = report_gen

    def build_sentiment(self, sentiment: str) -> None:
        self._report.sentiment = sentiment

class ReportDirector:
    """
    Director class for building reports
    """
    
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> AbstractReportBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: AbstractReportBuilder) -> None:
        """
        Setter for the builder
        """
        self._builder = builder

    def build_full_report(self, user: str, llama: str, mbti: str, report_gen: str, sentiment: str) -> None:
        self.builder.build_user(user)
        self.builder.build_llama(llama)
        self.builder.build_mbti(mbti)
        self.builder.build_report_gen(report_gen)
        self.builder.build_sentiment(sentiment)
        return self._builder.report
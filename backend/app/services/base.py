from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.schemas import (
    SearchResult, RealtimePrice, KLineData, 
    FinancialIndicator, ValuationData, StockBasicInfo
)


class BaseDataService(ABC):
    """数据服务抽象基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """服务名称"""
        pass
    
    @property
    @abstractmethod
    def priority(self) -> int:
        """优先级，数字越小优先级越高"""
        pass
    
    @abstractmethod
    async def search_stocks(self, keyword: str) -> List[SearchResult]:
        """搜索股票"""
        pass
    
    @abstractmethod
    async def get_realtime_price(self, codes: List[str]) -> List[RealtimePrice]:
        """获取实时价格"""
        pass
    
    @abstractmethod
    async def get_kline_data(
        self, 
        code: str, 
        period: str = "daily",
        adjust: str = "qfq",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[KLineData]:
        """获取K线数据"""
        pass
    
    @abstractmethod
    async def get_stock_basic_info(self, code: str) -> Optional[StockBasicInfo]:
        """获取股票基本信息"""
        pass
    
    @abstractmethod
    async def get_financial_indicators(
        self, 
        code: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[FinancialIndicator]:
        """获取财务指标"""
        pass
    
    @abstractmethod
    async def get_valuation_data(self, code: str) -> Optional[ValuationData]:
        """获取估值数据"""
        pass
    
    async def is_available(self) -> bool:
        """检查服务是否可用"""
        return True


class DataServiceRegistry:
    """数据服务注册器"""
    
    def __init__(self):
        self._services: Dict[str, List[BaseDataService]] = {}
    
    def register(self, service: BaseDataService):
        """注册数据服务"""
        if service.name not in self._services:
            self._services[service.name] = []
        self._services[service.name].append(service)
    
    def get_service(self, name: str) -> Optional[BaseDataService]:
        """获取指定名称的服务"""
        services = self._services.get(name, [])
        if services:
            # 返回优先级最高的服务
            return min(services, key=lambda s: s.priority)
        return None
    
    def get_all_services(self) -> List[BaseDataService]:
        """获取所有服务"""
        all_services = []
        for services in self._services.values():
            all_services.extend(services)
        return sorted(all_services, key=lambda s: s.priority)
    
    def get_primary_service(self) -> Optional[BaseDataService]:
        """获取主服务（优先级最高的）"""
        all_services = self.get_all_services()
        return all_services[0] if all_services else None


# 全局注册器实例
_registry = DataServiceRegistry()


def get_registry() -> DataServiceRegistry:
    return _registry


def register_service(service: BaseDataService):
    _registry.register(service)

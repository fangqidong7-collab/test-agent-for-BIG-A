"""
搜索API
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from ..models.schemas import SearchResponse, SearchResult
from ..services.base import get_registry

router = APIRouter(prefix="/api/search", tags=["search"])
logger = logging.getLogger(__name__)


@router.get("", response_model=SearchResponse)
async def search_stocks(q: str):
    """
    搜索股票
    
    支持按股票代码、股票简称、公司全名搜索
    """
    if not q or len(q) < 1:
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")
    
    if len(q) > 50:
        raise HTTPException(status_code=400, detail="搜索关键词过长")
    
    results = []
    seen_codes = set()
    
    # 遍历所有数据服务
    registry = get_registry()
    for service in registry.get_all_services():
        try:
            if await service.is_available():
                service_results = await service.search_stocks(q)
                
                # 去重
                for result in service_results:
                    if result.code not in seen_codes:
                        seen_codes.add(result.code)
                        results.append(result)
                
                # 找到足够结果就停止
                if len(results) >= 20:
                    break
        except Exception as e:
            logger.warning(f"{service.name} search failed: {e}")
    
    # 如果没有找到结果，返回友好提示
    if not results:
        logger.info(f"No results for query: {q}")
    
    return SearchResponse(
        stocks=results[:20],
        total=len(results),
        query=q
    )

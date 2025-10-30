from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from shared.config import settings

app = FastAPI(
    title="API Gateway",
    version="1.0.0",
    description="API Gateway for Microservices",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def forward_request(request: Request, call_next):
    """Forward requests to appropriate microservice"""
    path = request.url.path
    method = request.method
    
    # Determine target service
    if path.startswith("/api/auth"):
        target_url = settings.AUTH_SERVICE_URL
    elif path.startswith("/api/users"):
        target_url = settings.USER_SERVICE_URL
    elif path.startswith("/api/health"):
        target_url = settings.HEALTH_DATA_SERVICE_URL
    elif path.startswith("/api/ai"):
        target_url = settings.AI_SERVICE_URL
    else:
        # Default behavior for root and health
        response = await call_next(request)
        return response
    
    # Forward request
    async with httpx.AsyncClient() as client:
        url = f"{target_url}{path}"
        headers = dict(request.headers)
        headers.pop("host", None)
        
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, params=request.query_params)
            elif method == "POST":
                body = await request.body()
                response = await client.post(url, headers=headers, content=body)
            elif method == "PUT":
                body = await request.body()
                response = await client.put(url, headers=headers, content=body)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                response = await client.request(method, url, headers=headers)
            
            return StreamingResponse(
                iter([response.content]),
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get("content-type")
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "api-gateway",
        "version": "1.0.0",
        "status": "running",
        "routes": {
            "/api/auth": "Auth Service",
            "/api/users": "User Service",
            "/api/health": "Health Data Service",
            "/api/ai": "AI Service"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}


from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.schemas.jenkins import (
    BuildInfo,
    BuildLogResponse,
    JenkinsHealth,
    JobInfo,
    TriggerBuildRequest,
    TriggerBuildResponse,
)
from app.services.jenkins_service import jenkins_service
from app.services.timeline_service import timeline_service

router = APIRouter()


def _demo_health() -> JenkinsHealth:
    return JenkinsHealth(
        healthy=True,
        version="2.426.3",
        total_jobs=8,
        running_builds=1,
        queued_builds=0,
        failed_jobs_24h=1,
        success_rate_24h=87.5,
    )


def _demo_jobs() -> List[JobInfo]:
    return [
        JobInfo(name="kubesight-frontend-build", url="http://jenkins.local/job/kubesight-frontend-build", color="blue", buildable=True, last_build_number=142, last_successful_build=142, last_failed_build=139, health_score=80, description="Build and deploy frontend app"),
        JobInfo(name="kubesight-backend-build", url="http://jenkins.local/job/kubesight-backend-build", color="blue", buildable=True, last_build_number=98, last_successful_build=98, last_failed_build=95, health_score=90, description="Build and deploy backend API"),
        JobInfo(name="integration-tests", url="http://jenkins.local/job/integration-tests", color="blue", buildable=True, last_build_number=76, last_successful_build=76, last_failed_build=74, health_score=85, description="Run integration test suite"),
        JobInfo(name="deploy-staging", url="http://jenkins.local/job/deploy-staging", color="blue", buildable=True, last_build_number=63, last_successful_build=63, last_failed_build=None, health_score=100, description="Deploy to staging environment"),
        JobInfo(name="deploy-production", url="http://jenkins.local/job/deploy-production", color="blue", buildable=True, last_build_number=41, last_successful_build=41, last_failed_build=38, health_score=75, description="Deploy to production cluster"),
        JobInfo(name="security-scan", url="http://jenkins.local/job/security-scan", color="yellow", buildable=True, last_build_number=55, last_successful_build=54, last_failed_build=55, health_score=60, description="Run Trivy security scan on images"),
        JobInfo(name="database-backup", url="http://jenkins.local/job/database-backup", color="blue", buildable=True, last_build_number=365, last_successful_build=365, last_failed_build=None, health_score=100, description="Daily database backup job"),
        JobInfo(name="cleanup-old-images", url="http://jenkins.local/job/cleanup-old-images", color="blue", buildable=True, last_build_number=30, last_successful_build=30, last_failed_build=None, health_score=100, description="Clean up old Docker images from registry"),
    ]


@router.get("/health", response_model=JenkinsHealth)
async def get_jenkins_health():
    """Get Jenkins server health status."""
    try:
        return await jenkins_service.get_health()
    except Exception:
        return _demo_health()


@router.get("/jobs", response_model=List[JobInfo])
async def list_jobs(folder: Optional[str] = Query(None)):
    """List all Jenkins jobs."""
    try:
        return await jenkins_service.get_jobs(folder)
    except Exception:
        return _demo_jobs()


@router.get("/jobs/{job_name}", response_model=JobInfo)
async def get_job(job_name: str):
    """Get details of a specific job."""
    try:
        return await jenkins_service.get_job(job_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_name}/builds/{build_number}", response_model=BuildInfo)
async def get_build(job_name: str, build_number: int):
    """Get details of a specific build."""
    try:
        return await jenkins_service.get_build(job_name, build_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_name}/builds/{build_number}/log", response_model=BuildLogResponse)
async def get_build_log(job_name: str, build_number: int):
    """Get console output of a build."""
    try:
        log = await jenkins_service.get_build_log(job_name, build_number)
        truncated = len(log) > 100000
        if truncated:
            log = log[-100000:]
        return BuildLogResponse(job_name=job_name, build_number=build_number, log=log, truncated=truncated)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs/{job_name}/build", response_model=TriggerBuildResponse)
async def trigger_build(job_name: str, request: Optional[TriggerBuildRequest] = None):
    """Trigger a new build for a job."""
    try:
        parameters = request.parameters if request else {}
        queue_id = await jenkins_service.trigger_build(job_name, parameters)
        return TriggerBuildResponse(job_name=job_name, queue_id=queue_id, message=f"Build queued for {job_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs/{job_name}/builds/{build_number}/stop")
async def stop_build(job_name: str, build_number: int):
    """Stop a running build."""
    try:
        success = await jenkins_service.stop_build(job_name, build_number)
        return {"success": success, "message": f"Stopped build #{build_number}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queue")
async def get_queue():
    """Get current build queue."""
    try:
        return await jenkins_service.get_queue_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from unittest import mock
import re

from tests.providers.gcp.gcp_fixtures import GCP_PROJECT_ID, set_mocked_gcp_provider

class TestCloudStorageBucketPublicAccess:
    def test_bucket_public_access(self):
        cloudstorage_client = mock.MagicMock()
        
        cloudstorage_client.project_ids = [GCP_PROJECT_ID]
        cloudstorage_client.region = "global"

        from prowler.providers.gcp.services.cloudstorage.cloudstorage_service import Bucket

        cloudstorage_client.buckets = [Bucket(
            name="bucket1",
            id="bucket1",
            region="US",
            uniform_bucket_level_access=True,
            public=True,
            project_id=GCP_PROJECT_ID,
        )]

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_gcp_provider(),
        ), mock.patch(
            "prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_public_access.cloudstorage_bucket_public_access.cloudstorage_client",
            new=cloudstorage_client,
        ):
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_public_access.cloudstorage_bucket_public_access import cloudstorage_bucket_public_access

            check = cloudstorage_bucket_public_access()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert re.search("Bucket .* is publicly accessible", result[0].status_extended)
            assert result[0].resource_id == "bucket1"

    def test_bucket_no_public_access(self):
        cloudstorage_client = mock.MagicMock()
        
        cloudstorage_client.project_ids = [GCP_PROJECT_ID]
        cloudstorage_client.region = "global"

        from prowler.providers.gcp.services.cloudstorage.cloudstorage_service import Bucket

        cloudstorage_client.buckets = [Bucket(
            name="bucket2",
            id="bucket2",
            region="US",
            uniform_bucket_level_access=True,
            public=False,
            project_id=GCP_PROJECT_ID,
        )]

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_gcp_provider(),
        ), mock.patch(
            "prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_public_access.cloudstorage_bucket_public_access.cloudstorage_client",
            new=cloudstorage_client,
        ):
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_public_access.cloudstorage_bucket_public_access import cloudstorage_bucket_public_access

            check = cloudstorage_bucket_public_access()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert re.search("Bucket .* is not publicly accessible", result[0].status_extended)
            assert result[0].resource_id == "bucket2"

    def test_no_buckets(self):
        cloudstorage_client = mock.MagicMock()
        logging_client = mock.MagicMock()
        
        cloudstorage_client.project_ids = [GCP_PROJECT_ID]
        cloudstorage_client.region = "global"
        logging_client.sinks = [mock.MagicMock(destination="storage.googleapis.com/bucket1")]

        cloudstorage_client.buckets = []

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=set_mocked_gcp_provider(),
        ), mock.patch(
            "prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_public_access.cloudstorage_bucket_public_access.cloudstorage_client",
            new=cloudstorage_client,
        ):
            from prowler.providers.gcp.services.cloudstorage.cloudstorage_bucket_public_access.cloudstorage_bucket_public_access import (
                cloudstorage_bucket_public_access,
            )

            check = cloudstorage_bucket_public_access()
            result = check.execute()

            assert len(result) == 0        
import os.path

from aws_cdk import aws_cloudfront, aws_iam, aws_s3, aws_s3_deployment, core


class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        web_app_root = os.path.realpath(os.path.join(os.path.curdir, "..", "web"))

        bucket = aws_s3.Bucket(self, "Bucket", website_index_document="index.html")

        origin = aws_cloudfront.CfnCloudFrontOriginAccessIdentity(
            self,
            "BucketOrigin",
            cloud_front_origin_access_identity_config={"comment": "mythical-mysfists"},
        )
        bucket.grant_read(
            aws_iam.CanonicalUserPrincipal(origin.attr_s3_canonical_user_id)
        )

        cloudfront_distribution = aws_cloudfront.CloudFrontWebDistribution(
            self,
            "CloudFront",
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.ALLOW_ALL,
            price_class=aws_cloudfront.PriceClass.PRICE_CLASS_ALL,
            origin_configs=[
                {
                    "behaviors": [{"isDefaultBehavior": True, "max_ttl_seconds": None}],
                    "originPath": "/web",
                    "s3OriginSource": aws_cloudfront.S3OriginConfig(
                        s3_bucket_source=bucket, origin_access_identity_id=origin.ref
                    ),
                }
            ],
        )

        aws_s3_deployment.BucketDeployment(
            self,
            "DeployWebsite",
            source=aws_s3_deployment.Source.asset(web_app_root),
            destination_key_prefix="web/",
            destination_bucket=bucket,
            retain_on_delete=False,
        )

        core.CfnOutput(
            self,
            "CloudFrontURL",
            description="The CloudFront distribution URL",
            value="https://{}".format(cloudfront_distribution.domain_name),
        )

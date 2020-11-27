package com.rwang5688.file;

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.core.SdkSystemSetting;
import software.amazon.awssdk.services.s3.S3Client;

public final class S3Connection {
    private S3Client s3 = null;

    public S3Connection() {
        Region region = Region.of(System.getenv(SdkSystemSetting.AWS_REGION.environmentVariable()));
        s3 = S3Client.builder()
                        .region(region)
                        .build();
    }

    public void finalize() {
        s3.close();
    }

    public S3Client getS3() {
        return s3;
    }
}


package com.rwang5688.dal;

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.core.SdkSystemSetting;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;

public final class DynamoDBConnection {
    private DynamoDbClient db = null;
    private DynamoDbEnhancedClient enhancedClient = null;

    public DynamoDBConnection() {
        Region region = Region.of(System.getenv(SdkSystemSetting.AWS_REGION.environmentVariable()));
        db = DynamoDbClient.builder()
                            .region(region)
                            .build();
    }

    public void finalize() {
        db.close();
    }

    public DynamoDbClient getDb() {
        return db;
    }

    public DynamoDbEnhancedClient getEnhancedClient() {
        if (enhancedClient == null)
            enhancedClient = DynamoDbEnhancedClient.builder()
                                                    .dynamoDbClient(this.db)
                                                    .build();
        return enhancedClient;
    }
}


import os


def get_bucket_name_from_env_var(env_var_name):
    bucket_name = ''
    if env_var_name in os.environ:
        bucket_name = os.environ[env_var_name]
    print('get_bucket_name_from_env_var: env_var_name=%s, bucket_name=%s.' % (env_var_name, bucket_name))
    return bucket_name


def get_region_name():
    region_name = ''
    if 'REGION' in os.environ:
        region_name = os.environ['REGION']
    print('get_region_name: region_name=%s' % region_name)
    return region_name


def get_base_url(env_var_name):
    bucket_name = get_bucket_name_from_env_var(env_var_name)
    region_name = get_region_name()

    cloud_name = ''
    if 'CLOUD' in os.environ:
        cloud_name = os.environ['CLOUD']
    print('get_base_url: cloud_name=%s' % cloud_name)

    s3_region_separator = ""
    domain_name = ""
    if cloud_name == "aws":
        s3_region_separator = "-"
        domain_name = "amazonaws.com"
    elif cloud_name == "aws-cn":
        s3_region_separator = "."
        domain_name = "amazonaws.com.cn"
    else:
        print('get_base_url: Missing or unrecognized cloud name.')

    base_url = "https://" + bucket_name + ".s3" + s3_region_separator + \
                region_name + "." + domain_name + "/"
    print('get_base_url: base_url=%s' % base_url)

    return base_url


def generate_data_bucket_object_url(env_var_name, user_id, task_id, object_name):
    base_url = get_base_url(env_var_name)
    url = base_url + user_id + "/" + task_id + "/" + object_name
    print('generate_data_bucket_object_url: url=%s' % url)
    return url


def generate_preprocess_data_bucket_object_url(user_id, task_id, object_name):
    url = generate_data_bucket_object_url('PREPROCESS_DATA_BUCKET', user_id, task_id, object_name)
    return url


def generate_log_data_bucket_object_url(user_id, task_id, object_name):
    url = generate_data_bucket_object_url('LOG_DATA_BUCKET', user_id, task_id, object_name)
    return url


def generate_result_data_bucket_object_url(user_id, task_id, object_name):
    url = generate_data_bucket_object_url('RESULT_DATA_BUCKET', user_id, task_id, object_name)
    return url


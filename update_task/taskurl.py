import os


def get_bucket_name_from_env_var(env_var_name):
    bucket_name = ''
    if env_var_name in os.environ:
        bucket_name = os.environ[env_var_name]
    print(f'get_bucket_name: env_var_name={env_var_name}, bucket_name={bucket_name}.')
    return bucket_name


def get_region_name():
    region_name = ''
    if 'REGION' in os.environ:
        region_name = os.environ['REGION']
    print(f'get_region_name: region_name={region_name}')
    return region_name


def get_domain_name():
    cloud_name = ''
    if 'CLOUD' in os.environ:
        cloud_name = os.environ['CLOUD']
    print(f'get_domain_name: cloud_name={cloud_name}')

    domain_name = ''
    if cloud_name == 'aws':
        domain_name = 'amazonaws.com'
    elif cloud_name == 'aws-cn':
        domain_name = 'amazonaws.com.cn'
    else:
        print('get_domain_name: Missing or unrecognized cloud name.')
    print(f'get_domain_name: domain_name={domain_name}')
    return domain_name


def generate_data_bucket_object_url(env_var_name, user_id, task_id, object_name):
    bucket_name = get_bucket_name_from_env_var(env_var_name)
    region_name = get_region_name()
    domain_name = get_domain_name()
    url = "https://" + bucket_name + ".s3-" + region_name + "." + domain_name + "/"
    url = url + user_id + "/" + task_id + "/" + object_name
    print(f'generate_task_log_bucket_object_url: {url}')
    return url


def generate_log_data_bucket_object_url(user_id, task_id, object_name):
    url = generate_data_bucket_object_url('LOG_DATA_BUCKET', user_id, task_id, object_name)
    return url


def generate_result_data_bucket_object_url(user_id, task_id, object_name):
    url = generate_data_bucket_object_url('RESULT_DATA_BUCKET', user_id, task_id, object_name)
    return url


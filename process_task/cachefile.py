import s3util


def get_task_attribute_value(task, task_attribute_name):
    task_attribute_value = ''
    if task_attribute_name in task:
        task_attribute_value = task[task_attribute_name]
    else:
        print('get_task_attribute_value: Task attribute %s is not defined.' % task_attribute_name)

    return task_attribute_value


def get_cache_file_blob(bucket_name, task, \
    cache_name, cache_id_attribute_name, cache_file_attribute_name):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('get_cache_file_blob: Bucket %s does not exist.' % bucket_name)
        return None

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return None

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return None

    # get {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    cache_file_object = s3util.get_file_object(bucket_name, cache_file_object_name)
    if cache_file_object is None:
        print('get_cache_file_blob: Failed to get file object %s' % cache_file_object_name)
        return None

    # debug
    print('get_cache_file_blob: Got file object %s.' % cache_file_object_name)

    # extract blob from object
    cache_file_blob = cache_file_object['Body'].read()
    return cache_file_blob


def upload_cache_file(bucket_name, task, \
    cache_name, cache_id_attribute_name, cache_file_attribute_name, \
    local_cache_dir=""):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('upload_cache_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return ''

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return ''

    # upload {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    upload_file_name = local_cache_dir + cache_file_name
    success = s3util.upload_file(upload_file_name, bucket_name, cache_file_object_name)
    if not success:
        print('upload_cache_file: Failed to upload file %s.' % cache_file_name)
        return ''

    # success
    return upload_file_name


def download_cache_file(bucket_name, task, \
    cache_name, cache_id_attribute_name, cache_file_attribute_name, \
    local_cache_dir=""):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('download_cache_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return ''

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return ''

    # download {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    download_file_name = local_cache_dir + cache_file_name
    success = s3util.download_file(bucket_name, cache_file_object_name, download_file_name)
    if not success:
        print('download_cache_file: Failed to download file %s.' % cache_file_name)
        return ''

    # success
    return download_file_name


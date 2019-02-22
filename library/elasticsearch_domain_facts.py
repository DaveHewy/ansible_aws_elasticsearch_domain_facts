#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}


DOCUMENTATION = '''
---
module: elasticsearch_domain_facts
short_description: Get information about elasticsearch_domain
description:
    - Module search for Elasticsearch Domain (clusters)
version_added: "2.7"
requirements: [ boto3 ]
options:
    domain_name:
        description:
            - DomainName of the ES cluster.
    tags:
        description:
            - List of tags of ES. Should be defined as dictionary
extends_documentation_fragment:
  - aws
'''

EXAMPLES = '''
- elasticsearch_domain_facts:
    domain_name: example-domain
'''

RETURN = '''
elasticsearch_domain

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/es.html#ElasticsearchService.Client.describe_elasticsearch_domain
'''


try:
    import botocore
except ImportError:
    pass  # caught by AnsibleAWSModule

from ansible.module_utils.aws.core import AnsibleAWSModule
from ansible.module_utils._text import to_native
from ansible.module_utils.ec2 import boto3_conn, get_aws_connection_info, ec2_argument_spec


def get_elasticsearch_domain(module, client):
    """[summary]

    [description]

    Arguments:
        module {[type]} -- [description]
        client {[type]} -- [description]
    """
    try:
        domain_name = module.params.get('domain_name')
        return client.describe_elasticsearch_domain(DomainName=domain_name)
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e, msg='Unexpected error {0}'.format(to_native(e)))


def main():
    """
     Module action handler
    """
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
        id=dict(),
        domain_name=dict(),
        tags=dict(type="dict", default={}),
    ))

    module = AnsibleAWSModule(argument_spec=argument_spec,
                              supports_check_mode=True)

    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
    client = boto3_conn(
        module,
        conn_type='client',
        resource='es',
        region=region,
        endpoint=ec2_url,
        **aws_connect_kwargs)

    # only support pre-constructed domain_name or now
    es_domain = get_elasticsearch_domain(module, client)

    module.exit_json(changed=False, ansible_facts={'elasticsearch_domain': es_domain})


if __name__ == '__main__':
    main()

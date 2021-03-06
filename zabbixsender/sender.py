#!/usr/bin/env python
import struct
import json
import socket


class ZabbixSender:
    def __init__(self, zbx_server_host, zbx_server_port):
        self.zbx_server_host = zbx_server_host
        self.zbx_server_port = zbx_server_port
        self.zbx_header = 'ZBXD'
        self.zbx_protocols_version = 1
        self.zbx_send_value = {'request': 'sender data', 'data': []}
        self.zbx_send_data = ''

    def adddata(self, host, key, value):
        add_data = {'host': host, 'key': key, 'value': value}
        self.zbx_send_value['data'].append(add_data)

    def makesenddata(self):
        zbx_send_json = json.dumps(self.zbx_send_value)
        zbx_send_json_len = len(zbx_send_json)
        self.zbx_send_data = struct.pack("<4sBq" + str(zbx_send_json_len) + "s", 'ZBXD', 1, zbx_send_json_len,
                                         zbx_send_json)

    def send(self):
        self.makesenddata()
        zbx_server_socket = socket.socket()
        zbx_server_socket.connect((self.zbx_server_host, self.zbx_server_port))
        zbx_server_write_df = zbx_server_socket.makefile('wb')
        zbx_server_write_df.write(self.zbx_send_data)
        zbx_server_write_df.close()
        zbx_server_read_df = zbx_server_socket.makefile('rb')
        zbx_response_package = zbx_server_read_df.read()
        zbx_server_read_df.close()
        zbx_response_data = struct.unpack("<4sBq" + str(len(zbx_response_package) - struct.calcsize("<4sBq")) + "s",
                                          zbx_response_package)
        return zbx_response_data[3]


if __name__ == '__main__':
    zabbix_sender = ZabbixSender('10.16.7.188', 10051)
    zabbix_sender.adddata('solrmaster', 'get_number_of_solr_index_update', 60)
    response = zabbix_sender.send()
    print response

import xml.etree.ElementTree as ET
 
# 创建根元素
test_suite = ET.Element('testsuite')
test_suite.set('name', 'ExampleTestSuite')
 
# 添加一个测试用例
test_case = ET.SubElement(test_suite, 'testcase')
test_case.set('name', 'ExampleTestCase')
 
# 添加一个失败的测试
test_case_failure = ET.SubElement(test_suite, 'testcase')
test_case_failure.set('name', 'FailingTestCase')
failure = ET.SubElement(test_case_failure, 'failure')
failure.set('message', 'Test failed')
 
# 添加一个错误的测试
test_case_error = ET.SubElement(test_suite, 'testcase')
test_case_error.set('name', 'ErrorTestCase')
error = ET.SubElement(test_case_error, 'error')
error.set('message', 'Test errored')
 
# 生成XML
xml_data = ET.tostring(test_suite, encoding='utf8', method='xml')
xml_str = str(xml_data, 'utf-8')
print(xml_str)

# 创建XML并保存到文件
tree = ET.ElementTree(test_suite)
tree.write("test_report.xml", encoding="utf-8", xml_declaration=True)

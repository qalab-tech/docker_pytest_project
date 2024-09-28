import grpc
import grpc_testing
import pytest

from customer_pb2 import CreateCustomerRequest, CreateCustomerResponse
from customer_pb2_grpc import CustomerServiceStub, add_CustomerServiceServicer_to_server, CustomerServiceServicer


# Mock-service CustomerService implementation:
class MockCustomerService(CustomerServiceServicer):
    def CreateCustomer(self, request, context):
        # Mock-server main logic
        if request.name and request.address:
            return CreateCustomerResponse(customer_id="123456")
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid data")


@pytest.fixture
def grpc_mock_channel():
    """Creating mock-channel and mock-server"""
    servicers = {
        CustomerServiceStub: MockCustomerService()
    }

    # Creating mock-channel and mock-server using grpc_testing
    real_time = grpc_testing.strict_real_time()
    server = grpc_testing.server_from_dictionary(
        {CustomerServiceStub: MockCustomerService()}, real_time)

    return server.invoke_unary_unary(
        method_descriptor=CustomerServiceStub.CreateCustomer,
        invocation_metadata={})


def test_create_customer(grpc_mock_channel):
    """Mockserver gRPC test"""
    request = CreateCustomerRequest(name="Test User", address="1234 Test St")
    response = grpc_mock_channel.CustomerService.CreateCustomer(request)

    # Assert Response
    assert response.customer_id == "123456"

# BrowserSimulator
class BrowserSimulatorError(Exception):
    """
    Base class for exceptions in BrowserSimulator class 
    """

class ExecutionError(BrowserSimulatorError):
    """
    Exception raised when there's an error in executing script in BrowserSimulator.
    """

class NoPageAvailableError(BrowserSimulatorError):
    """
    Exception raised when trying to visit a URL but there's no page available.
    """

class NoContentAvailableError(BrowserSimulatorError):
    """
    Exception raised when trying to get content but there's no content available.
    """

# AttackerOPClient
class AttackerOPClientError(Exception):
    """
    Base class for exceptions in AttackerOPClient class 
    """

class AddTaskError(AttackerOPClientError):
    """
    Exception raised when there's an error in adding task in AttackerOPClient.
    """

class GetTaskError(AttackerOPClientError):
    """
    Exception raised when there's an error in getting task in AttackerOPClient.
    """

class DeleteTaskError(AttackerOPClientError):
    """
    Exception raised when there's an error in deleting task in AttackerOPClient.
    """

class ReplaceIdTokenError(AttackerOPClientError):
    """
    Exception raised when there's an error in replacing ID token in AttackerOPClient.
    """

class SetMaliciousEndpointsError(AttackerOPClientError):
    """
    Exception raised when there's an error in setting malicious endpoints in AttackerOPClient.
    """

class IdPConfusionError(AttackerOPClientError):
    """
    Exception raised when there's an error in IDP confusion in AttackerOPClient.
    """

class CleanError(AttackerOPClientError):
    """
    Exception raised when there's an error in cleaning in AttackerOPClient.
    """

# ProxyClient
class ProxyClientError(Exception):
    """
    Base class for exceptions in ProxyClient class 
    """

class SendDataError(ProxyClientError):
    """
    Exception raised when there's an error in sending data in ProxyClient.
    """

class CLIClientError(Exception):
    """
    Base class for exceptions in CLIClient class 
    """

class SendResultError(CLIClientError):
    """
    Exception raised when there's an error in sending results in CLIClient.
    """

# RequestBin
class RequestBinError(Exception):
    """
    Base class for exceptions in RequestBin class 
    """
class GetHistoryError(RequestBinError):
    """
    Exception raised when there's an error in getting history in RequestBin.
    """
# -*- coding: utf-8 -*-
#
# SonyAPI
# External control of Sony Bravia Generation 3 TV's
# Copyright (C) 2017  Kevin G. Schlosser
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import absolute_import
from .logger import LOGGER as _LOGGER
import json


class SonyAPIError(Exception):
    __module__ = 'SonyAPI'
    _msg = ''

    def __init__(self, err, debug_data=''):
        self._err = err
        if isinstance(debug_data, dict):
            debug_data = json.dumps(debug_data, indent=4)

        _LOGGER.error(self.__class__.__name__, debug_data)

    def __getitem__(self, item):
        return self._err[item]

    def __str__(self):
        return 'message: {0}\nerror: {2}\nerror id: {1}'.format(
            self._msg,
            *self._err
        )


class UnauthorizedError(SonyAPIError):
    _msg = 'The request requires user authentication.'


class ForbiddenError(SonyAPIError):
    _msg = (
        'The server understood the request, but is refusing to fulfill it. '
        'Client does not have permission to access.'
    )


class APINotFoundError(SonyAPIError):
    _msg = (
        'For cases where request is not matched to any supported API version.'
    )


class RequestEntityTooLargeError(SonyAPIError):
    _msg = (
        'The accepted body size of a client request exceeds maximum.'
    )


class RequestURITooLongError(SonyAPIError):
    _msg = (
        'The accepted URI length of a client request exceeds maximum.'
    )


class NotImplementedError(SonyAPIError):
    _msg = (
        'Requested item is not implemented on the server.'
    )


class ServiceUnavailable(SonyAPIError):
    _msg = (
        'When server is in temporally unavailable state which may occur due '
        'to over concurrent connections. (We don\'t define the number of max '
        'connections because it depends on servers.)'
    )


class TimeoutError(SonyAPIError):
    _msg = (
        'Server can not reply in time.'
    )


class IllegalArgumentError(SonyAPIError):
    _msg = (
        '"params" value in request does not follow API specification.'
    )


class IllegalRequestError(SonyAPIError):
    _msg = (
        'Request body is empty, has no id or invalid id, has no method, has '
        'no params, or params is not an array.'
    )


class IllegalStateError(SonyAPIError):
    _msg = (
        'Server can not handle the request at this time.'
    )


class NoSuchMethodError(SonyAPIError):
    _msg = (
        'Requested API does not exist.'
    )


class UnsupportedVersionError(SonyAPIError):
    _msg = (
        'Requested version is not supported in the specified service.'
    )


class UnsupportedOperationError(SonyAPIError):
    _msg = (
        'Server can not handle the request with respect to the specified '
        'parameters.'
    )


class RequestRetryError(SonyAPIError):
    _msg = (
        'Long Polling timeout.'
    )


class ClientOverMaximumError(SonyAPIError):
    _msg = (
        'The number of Long Polling client exceeds maximum.'
    )


class EncryptionFailedError(SonyAPIError):
    _msg = (
        'Failed to encrypt/decrypt in encryption API.'
    )


class RequestDuplicatedError(SonyAPIError):
    _msg = (
        'A client must wait for previous response.'
    )


class MultipleSettingsError(SonyAPIError):
    _msg = (
        'One or more settings are not set by error when multiple settings are '
        'set. Client needs to call paired APIs (getXXXSettings) to identify '
        'which parameters fail to be updated.'
    )


class DisplayTurnedOffError(SonyAPIError):
    _msg = (
        'Display is turned off.'
    )


class ShootingFailError(SonyAPIError):
    _msg = (
        'Failed to photograph.'
    )


class CameraNotReadyError(SonyAPIError):
    _msg = (
        'Camera is not ready.'
    )


class AlreadyRunningPollingAPIError(SonyAPIError):
    _msg = (
        'Already Running Polling API.'
    )


class CapturingNotFinishedError(SonyAPIError):
    _msg = (
        'Capturing has Not Finished.'
    )


class ScreenChangeError(SonyAPIError):
    _msg = (
        'Another request in progress.'
    )


class TargetNotSupportedError(SonyAPIError):
    _msg = (
        'Target is not supported or can not be controlled for some device '
        'specific reason.'
    )


class VolumeOutOfRangeError(SonyAPIError):
    _msg = (
        'Volume is out of range.'
    )


class ContentProtectedError(SonyAPIError):
    _msg = (
        'Content is protected.'
    )


class ContentExistError(SonyAPIError):
    _msg = (
        'Content does not exist.'
    )


class ContentStorageError(SonyAPIError):
    _msg = (
        'Storage has no content.'
    )


class ContentDeleteError(SonyAPIError):
    _msg = (
        'Some content could not be deleted.'
    )


class ChannelFixedByUSBError(SonyAPIError):
    _msg = (
        'Channel fixed by USB recording.'
    )


class ChannelFixedBySCARTError(SonyAPIError):
    _msg = (
        'Channel fixed by SCART recording.'
    )


class ChapterExistError(SonyAPIError):
    _msg = (
        'Chapter doesn\'t exist.'
    )


class ChannelUniqueError(SonyAPIError):
    _msg = (
        'Channel can’t be uniquely determined.'
    )


class EmptyChannelListError(SonyAPIError):
    _msg = (
        'Empty Channel list.'
    )


class StorageExistError(SonyAPIError):
    _msg = (
        'Storage doesn\'t exist.'
    )


class StorageFullError(SonyAPIError):
    _msg = (
        'Storage is full.'
    )


class ContentAttributeError(SonyAPIError):
    _msg = (
        'Content attribute setting failed.'
    )


class UnknownGroupIdError(SonyAPIError):
    _msg = (
        'Unknown group id.'
    )


class UnmatchedRequestError(SonyAPIError):
    _msg = (
        'Scheduled item specified in the request does not exist.'
    )


class AlreadyRecordingError(SonyAPIError):
    _msg = (
        'Middle of recording.'
    )


class ScheduleOverMaximumError(SonyAPIError):
    _msg = (
        'Device can not accept this item because number of registered items '
        'exceeds the capacity.'
    )


class ScheduleOverlapError(SonyAPIError):
    _msg = (
        'Timeline of this item overlaps w/ other items.'
    )


class DurationTooShortError(SonyAPIError):
    _msg = (
        'The duration of the scheduled item too short.'
    )


class EndTimePassedError(SonyAPIError):
    _msg = (
        'The end time of item has already passed.'
    )


class BCASError(SonyAPIError):
    _msg = (
        'Conditional access related error (Some device is possible to check '
        'this on registering item).'
    )


class ProgramNotFoundError(SonyAPIError):
    _msg = (
        'Program not found.'
    )


class CopyControlError(SonyAPIError):
    _msg = (
        'Recording not allowed due to copy control.'
    )


class ChannelNotContractedError(SonyAPIError):
    _msg = (
        'Channel is not contracted.'
    )


class ProgramRatingError(SonyAPIError):
    _msg = (
        'Failure due to rating information.'
    )


class ReminderAlreadyExistsError(SonyAPIError):
    _msg = (
        'Reminder already exists for this eventId.'
    )


class StartTimePassedError(SonyAPIError):
    _msg = (
        'The start time of item has already passed.'
    )


class ProgramShortStartError(SonyAPIError):
    _msg = (
        'Program will start in less than 30 seconds.'
    )


class StorageNotReadyError(SonyAPIError):
    _msg = (
        'Storage is not ready.'
    )


class StorageNotRegisteredError(SonyAPIError):
    _msg = (
        'Storage is not registered.'
    )


class EventNotContractedError(SonyAPIError):
    _msg = (
        'Event is not contracted.'
    )


class AnotherRequestInProgressError(SonyAPIError):
    _msg = (
        'Another request in progress.'
    )


class FailedToLaunchError(SonyAPIError):
    _msg = (
        'Failed to launch, for example, because another application is '
        'running.'
    )


class RequestInProgressError(SonyAPIError):
    _msg = (
        'Request is accepted, but the completion of application launch can '
        'not be decided.'
    )


class FailedToTerminateError(SonyAPIError):
    _msg = (
        'Some applications can\'t be terminated.'
    )


class CountOutOfRangeError(SonyAPIError):
    _msg = (
        'Specified count is out of range.'
    )


class IndexOutOfRangeError(SonyAPIError):
    _msg = (
        'Specified index is out of range.'
    )


class NotFoundError(SonyAPIError):
    _msg = (
        'Specified file is not found.'
    )


class WrongUUIDError(SonyAPIError):
    _msg = (
        'Specified uuid is invalid.'
    )


class WrongNicknameError(SonyAPIError):
    _msg = (
        'Specified nickname is invalid.'
    )


class CannotRegisterError(SonyAPIError):
    _msg = (
        'Client cannot be registered any more.'
    )


class StorageDBFullError(SonyAPIError):
    _msg = (
        'Database is full.'
    )


class E1000Error(SonyAPIError):
    _msg = (
        'General error with Error ID which is defined by system.'
    )


class KeyExistError(SonyAPIError):
    _msg = (
        'Key doesn\'t exist yet.'
    )


class ClientApplicationNotPairedError(SonyAPIError):
    _msg = (
        'Client application is not already paired.'
    )


class ServerNotInPairingModeError(SonyAPIError):
    _msg = (
        'Server device is not under pairing mode.'
    )


class LoginRequiredError(SonyAPIError):
    _msg = (
        'Client application needs log in operation.'
    )


class ClientAlreadyLoggedInError(SonyAPIError):
    _msg = (
        'Client has already logged in.'
    )


class RegistrationFullError(SonyAPIError):
    _msg = (
        'Registration full.'
    )


class RequestedOperationRejectedError(SonyAPIError):
    _msg = (
        'Requested operation was rejected by host.'
    )


class IdAlreadyAssignedError(SonyAPIError):
    _msg = (
        'ID can not be assigned due to server error.'
    )


class ClientInGroupError(SonyAPIError):
    _msg = (
        'Client has already joined the group.'
    )


class ClientNotAllowedInGroupError(SonyAPIError):
    _msg = (
        'Client does not join the group.'
    )


class GroupIdNotFoundError(SonyAPIError):
    _msg = (
        'Group ID not found.'
    )


class ApplicationInformationNotSetError(SonyAPIError):
    _msg = (
        'Application information is not set.'
    )


EXCEPTIONS = {
    401: UnauthorizedError,
    403: ForbiddenError,
    404: APINotFoundError,
    413: RequestEntityTooLargeError,
    414: RequestURITooLongError,
    501: NotImplementedError,
    503: ServiceUnavailable,
    2: TimeoutError,
    3: IllegalArgumentError,
    5: IllegalRequestError,
    7: IllegalStateError,
    12: NoSuchMethodError,
    14: UnsupportedVersionError,
    15: UnsupportedOperationError,
    40000: RequestRetryError,
    40001: ClientOverMaximumError,
    40002: EncryptionFailedError,
    40003: RequestDuplicatedError,
    40004: MultipleSettingsError,
    40005: DisplayTurnedOffError,
    40400: ShootingFailError,
    40401: CameraNotReadyError,
    40402: AlreadyRunningPollingAPIError,
    40403: CapturingNotFinishedError,
    40600: ScreenChangeError,
    40800: TargetNotSupportedError,
    40801: VolumeOutOfRangeError,
    41000: ContentProtectedError,
    41001: ContentExistError,
    41002: ContentStorageError,
    41003: ContentDeleteError,
    41011: ChannelFixedByUSBError,
    41012: ChannelFixedBySCARTError,
    41013: ChapterExistError,
    41014: ChannelUniqueError,
    41015: EmptyChannelListError,
    41020: StorageExistError,
    41021: StorageFullError,
    41022: ContentAttributeError,
    41023: UnknownGroupIdError,
    41200: UnmatchedRequestError,
    41201: AlreadyRecordingError,
    41221: ScheduleOverMaximumError,
    41222: ScheduleOverlapError,
    41223: DurationTooShortError,
    41224: EndTimePassedError,
    41225: BCASError,
    41226: ProgramNotFoundError,
    41227: CopyControlError,
    41228: ChannelNotContractedError,
    41229: ProgramRatingError,
    41230: ReminderAlreadyExistsError,
    41231: StartTimePassedError,
    41232: ProgramShortStartError,
    41233: StorageNotReadyError,
    41234: StorageNotRegisteredError,
    41235: EventNotContractedError,
    41400: AnotherRequestInProgressError,
    41401: FailedToLaunchError,
    41402: RequestInProgressError,
    41403: FailedToTerminateError,
    41801: CountOutOfRangeError,
    41802: IndexOutOfRangeError,
    41804: NotFoundError,
    41806: WrongUUIDError,
    41807: WrongNicknameError,
    42000: CannotRegisterError,
    42200: StorageDBFullError,
    42201: E1000Error,
    42202: KeyExistError,
    42600: ClientApplicationNotPairedError,
    42601: ServerNotInPairingModeError,
    42800: LoginRequiredError,
    42801: ClientAlreadyLoggedInError,
    42802: RegistrationFullError,
    42803: RequestedOperationRejectedError,
    42804: IdAlreadyAssignedError,
    42805: ClientInGroupError,
    42806: ClientNotAllowedInGroupError,
    42807: GroupIdNotFoundError,
    42808: ApplicationInformationNotSetError
}


class PinError(SonyAPIError):
    __module__ = 'SonyAPI'


class RegisterTimeoutError(SonyAPIError):
    __module__ = 'SonyAPI'


class NotImplementedError(SonyAPIError):
    # 501,"Not Implemented"
    __module__ = 'SonyAPI'


class UnsupportedError(SonyAPIError):
    # 15, "unsupported"
    __module__ = 'SonyAPI'


class JSONRequestError(SonyAPIError):
    __module__ = 'SonyAPI'
    # 7, "Illegal State"
    # 7, "Clock is not set"
    # 12, "getLEDIndicatorStatus"

    def __init__(self, num, msg):
        self._num = num
        self._msg = msg

    def __str__(self):
        return 'error: %d, %s' % (self._num, self._msg)

    def __eq__(self, other):
        return other in (self._num, self._msg)


class CommandError(SonyAPIError):
    __module__ = 'SonyAPI'


class VolumeDeviceError(SonyAPIError):
    __module__ = 'SonyAPI'


class RegisterError(SonyAPIError):
    __module__ = 'SonyAPI'


class IRCCError(SonyAPIError):
    __module__ = 'SonyAPI'


class SendError(SonyAPIError):
    __module__ = 'SonyAPI'


class IPAddressError(SonyAPIError):
    __module__ = 'SonyAPI'

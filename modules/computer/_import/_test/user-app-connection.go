/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/authorization"
	"github.com/GeniusesGroup/libgo/protocol"
)

/*
Connection Authorization service
We have 2 types access to real user data.

Relations Access
Relations of users have many kind like friends(in many scope), followers, family(in many grade), ... . Relations have fixed types. These relations knowledge store in Relations MS.

Token Access
Users can make authentication token and give it to third party to access his/her data. So to restricted access, User can be set rules for tokens to limit to specific rules.
*/

// UserAppConnection ---Read locale description in userAppConnectionStructure---
type UserAppConnection struct {
	RequestID [32]byte // user-request domain

	/* Connection data */
	ID            [32]byte
	AppInstanceID [32]byte // Store to remember which app instance use this record tp prove user requests
	Weight        protocol.Weight
	Status        UserAppConnectionStatus

	/* Peer data */
	// Peer Location
	Addr     [16]byte
	AddrType protocol.NetworkLinkNextHeaderID
	// Peer Identifiers
	DomainName     string // if exist
	UserID         [16]byte
	DelegateUserID [16]byte

	/* Security data */
	PeerPublicKey [32]byte
	AccessControl authorization.AccessControl
}

// conn = &achaemenid.Connection{
// 	/* Connection data */
// 	ID:     uac.ID,
// 	State:  achaemenid.StateLoaded,
// 	Weight: uac.Weight,

// 	/* Peer data */
// 	// Peer Location
// 	GPAddr:  uac.GPAddr,
// 	IPAddr:  uac.IPAddr,
// 	ThingID: uac.ThingID,
// 	// Peer Identifiers
// 	UserID:           uac.UserID,
// 	UserType:         uac.UserType,
// 	DelegateUserID:   uac.DelegateUserID,
// 	DelegateUserType: uac.DelegateUserType,

// 	/* Security data */
// 	PeerPublicKey: uac.PeerPublicKey,
// 	// Cipher        crypto.Cipher
// 	AccessControl: uac.AccessControl,

// 	/* Metrics data */
// 	LastUsage:             uac.LastUsage,
// 	PacketPayloadSize:     uac.PacketPayloadSize,
// 	MaxBandwidth:          uac.MaxBandwidth,
// 	ServiceCallCount:      uac.ServiceCallCount,
// 	BytesSent:             uac.BytesSent,
// 	PacketsSent:           uac.PacketsSent,
// 	BytesReceived:         uac.BytesReceived,
// 	PacketsReceived:       uac.PacketsReceived,
// 	FailedPacketsReceived: uac.FailedPacketsReceived,
// 	FailedServiceCall:     uac.FailedServiceCall,
// }

// UserAppConnectionStatus use to indicate UserAppConnection record status
type UserAppConnectionStatus uint8

// UserAppConnection status
const (
	UserAppConnectionUnset UserAppConnectionStatus = iota
	UserAppConnectionIssued
	UserAppConnectionUpdate
	UserAppConnectionExpired
	UserAppConnectionRevoked
)

// UserPublicKey status
const (
	UserPublicKeyIssue_Unset UserPublicKeyStatus = iota
	UserPublicKeyIssueByPassword
	UserPublicKeyIssueByPasswordAndOTP
	UserPublicKeyIssueByPasswordAndIdentification
	UserPublicKeyIssueByPasswordAndOTPAndIdentification
	UserPublicKeyExpired
	UserPublicKeyRevoked
)

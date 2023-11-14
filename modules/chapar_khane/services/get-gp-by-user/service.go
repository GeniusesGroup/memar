/* For license and copyright information please see the LEGAL file in the code repository */

package ggbuService

import (
	cmd "memar/command"
	"memar/datatype"
	"memar/mediatype"
	"memar/service"
)

var Service serv

type serv struct {
	datatype.DataType
	mediatype.MT
	service.Service
	cmd.Command
}

// var getGPAddressService = service.Service{
// 	ID:                 0,
// 	Name:               "GetGPAddress",
// 	IssueDate:          0,
// 	ExpiryDate:         0,
// 	ExpireInFavorOfURN: "",
// 	ExpireInFavorOfID:  0,
// 	Status:             protocol.Software_PreAlpha,
// 	Handler:            GetGPAddress,
// 	Description: []string{
// 		`use to make new connection by ECC algorithm`,
// 	},
// 	TAGS: []string{},
// }

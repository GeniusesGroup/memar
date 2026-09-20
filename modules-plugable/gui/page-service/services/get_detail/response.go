/* For license and copyright information please see the LEGAL file in the code repository */

package gds

import (
	"encoding/json"

	"memar/protocol"
)

type response struct {
	JSON   []byte
	Syllab []byte
}

// Response store needed data for a service to implement protocol.Response when embed to other struct that implements other methods!
type Response struct {
	uri    string // Fill just if any http like type handler needed! Simple URI not variable included! API services can set like "/m?{{.ServiceID}}" but it is not efficient, find services by ID.
	status protocol.SoftwareStatus

	detail map[protocol.LanguageID]*ServiceDetail

	authorization Authorization
}

/*
*********** Service Encoders & Decoders ***********
 */

func (res *Response) FromSyllab() (err error_p.Error) {
	return
}

func (res *Response) ToSyllab() {
}

func (res *Response) LenOfSyllabStack() (ln uint32) {
	return
}

func (res *Response) LenOfSyllabHeap() (ln uint32) {
	return
}

func (res *Response) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *Response) jsonDecoder() (err error_p.Error) {
	json.Unmarshal(res.JSON, res)
	return
}

func (res *Response) ToJSON() {
	res.JSON, _ = json.Marshal(res)
}

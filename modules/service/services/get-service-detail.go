/* For license and copyright information please see the LEGAL file in the code repository */

package services

import (
	"memar/http"
	"memar/json"
	"memar/protocol"
	"memar/service"
	"memar/srpc"
	"memar/syllab"
)

var GetServiceDetailService = getServiceDetailService{
	Service: New("domain/service.protocol.service; name=get-service-detail", "", protocol.Software_PreAlpha, 1601109351).
		SetDetail(protocol.LanguageEnglish, "Get Service Detail",
			"Returns service all details by given service ID or URI",
			[]string{}).
		SetAuthorization(protocol.CRUDRead, protocol.UserType_All).Expired(0, ""),
}

type getServiceDetailService struct {
	service.Service
}

func (ser *getServiceDetailService) DO(st protocol.Stream, req *getServiceDetailReq) (res *getServiceDetailRes, err protocol.Error) {
	var service *service.Service
	if req.ServiceID != 0 {
		service = protocol.App.GetServiceByID(req.ServiceID)
	} else {
		service = protocol.App.GetServiceByURI(req.ServiceURI)
	}

	if service == nil {
		err = srpc.ErrServiceNotFound
	} else {
		res = &getServiceDetailRes{
			JSON:   service.JSON,
			Syllab: service.Syllab,
		}
	}
	return
}

func (ser *getServiceDetailService) DoSRPC(req GetServiceDetailServiceRequest) (res getServiceDetailServiceResponse, err protocol.Error) {
	return
}

func (ser *getServiceDetailService) DoHTTP(req GetServiceDetailServiceRequest) (res getServiceDetailServiceResponse, err protocol.Error) {
	return
}

func (ser *getServiceDetailService) ServeSRPC(st protocol.Stream, rawReq protocol.Codec) (rawRes protocol.Codec, err protocol.Error) {
	var req = &getServiceDetailReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getServiceDetailRes
	res, err = getServiceDetail(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		return
	}

	st.OutcomePayload = res.Syllab
}

func (ser *getServiceDetailService) ServeHTTP(st protocol.Stream, httpReq protocol.HTTPRequest, httpRes protocol.HTTPResponse) (err protocol.Error) {
	var req = &getServiceDetailReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getServiceDetailRes
	res, err = getServiceDetail(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.Body = res.JSON
	return
}

/*
	Service request and response shape
*/

type getServiceDetailServiceRequest interface {
	OrgID() [32]byte
	Offset() uint64
	Limit() uint64
}

type getServiceDetailServiceResponse interface {
	IDs() [][32]byte
}

/*
	Service Request
*/

type getServiceDetailReq struct {
	ServiceID  uint64
	ServiceURI string
}

type getServiceDetailRes struct {
	JSON   []byte
	Syllab []byte
}

/*
	Request Encoders & Decoders
*/

func (req *getServiceDetailReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.ServiceID = syllab.GetUInt64(buf, 0)
	req.ServiceURI = syllab.UnsafeGetString(buf, 8)
	return
}

func (req *getServiceDetailReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {
	syllab.SetUInt64(buf, 0, req.ServiceID)
	syllab.SetString(buf, req.ServiceURI, 8, heapIndex)
	return
}

func (req *getServiceDetailReq) LenOfSyllabStack() uint32 {
	return 16
}

func (req *getServiceDetailReq) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(req.ServiceURI))
	return
}

func (req *getServiceDetailReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *getServiceDetailReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ServiceID":
			req.ServiceID, err = decoder.DecodeUInt64()
		case "ServiceURI":
			req.ServiceURI, err = decoder.DecodeString()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *getServiceDetailReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ServiceID":`)
	encoder.EncodeUInt64(req.ServiceID)

	encoder.EncodeString(`,"ServiceURI":"`)
	encoder.EncodeString(req.ServiceURI)

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *getServiceDetailReq) LenAsJSON() (ln int) {
	ln = 60
	ln += len(req.ServiceURI)
	return
}

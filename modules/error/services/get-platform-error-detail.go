/* For license and copyright information please see the LEGAL file in the code repository */

package error

import (
	er "memar/error"
	"memar/http"
	"memar/json"
	lang "memar/language"
	"memar/srpc"
	"memar/syllab"
)

var getPlatformErrorDetailService = service.Service{
	URN:                "domain/achaemenid.protocol.service; name=get-platform-error-detail",
	Domain:             DomainName,
	ID:                 8746018193450136356,
	IssueDate:          1601109379,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Detail: map[protocol.LanguageID]service.ServiceDetail{
		protocol.LanguageEnglish: {
			Name:                                           "Get Platform Error Detail",
			Description: "Returns error all details by given ID",
			TAGS:                                           []string{},
		},
	},

	SRPCHandler: GetPlatformErrorDetailSRPC,
	ServeHTTP: GetPlatformErrorDetailHTTP,
}

// GetPlatformErrorDetailSRPC is sRPC handler of GetPlatformErrorDetail service.
func GetPlatformErrorDetailSRPC(st protocol.Stream) {
	var req = &getPlatformErrorDetailReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res *getPlatformErrorDetailRes
	res, err = getPlatformErrorDetail(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		return
	}

	st.OutcomePayload = res.Syllab
}

// GetPlatformErrorDetailHTTP is HTTP handler of GetPlatformErrorDetail service.
func GetPlatformErrorDetailHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &getPlatformErrorDetailReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res *getPlatformErrorDetailRes
	res, err = getPlatformErrorDetail(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.Body = res.JSON
}

type getPlatformErrorDetailReq struct {
	ErrorID uint64
}

type getPlatformErrorDetailRes struct {
	JSON   []byte
	Syllab []byte
}

func getPlatformErrorDetail(st protocol.Stream, req *getPlatformErrorDetailReq) (res *getPlatformErrorDetailRes, err protocol.Error) {
	var er = protocol.App.GetErrorByID(req.ErrorID)
	res = &getPlatformErrorDetailRes{
		JSON:   er.JSON,
		Syllab: er.Syllab,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *getPlatformErrorDetailReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.ErrorID = syllab.GetUInt64(buf, 0)
	return
}

func (req *getPlatformErrorDetailReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32)
	syllab.SetUInt64(buf, 0, req.ErrorID)
	return
}

func (req *getPlatformErrorDetailReq) LenOfSyllabStack() uint32 {
	return 8
}

func (req *getPlatformErrorDetailReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *getPlatformErrorDetailReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *getPlatformErrorDetailReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "ErrorID":
			req.ErrorID, err = decoder.DecodeUInt64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *getPlatformErrorDetailReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"ErrorID":`)
	encoder.EncodeUInt64(req.ErrorID)

	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *getPlatformErrorDetailReq) LenAsJSON() (ln int) {
	ln = 42
	return
}


// FromSyllab decode syllab to given Error
func (e *Error) FromSyllab(payload []byte, stackIndex uint32) {

}

func (e *Error) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32) {

	return
}

// JSONDecoder decode json to given Error
func (e *Error) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	return
}

func (e *Error) ToJSON() (buf []byte) {
	buf = make([]byte, 0, e.LenAsJSON())

	buf = append(buf, `{"ID":`...)
	buf = append(buf, e.urn.IDasString()...)

	buf = append(buf, `,"Detail":{`...)
	if e.detail != nil {
		for key, value := range e.detail {
			buf = append(buf, '"')
			buf = strconv.AppendUint(buf, uint64(key), 10)
			buf = append(buf, `":{"Domain":"`...)
			buf = append(buf, value.domain...)
			buf = append(buf, `","Summary":"`...)
			buf = append(buf, value.summary...)
			buf = append(buf, `","Overview":"`...)
			buf = append(buf, value.overview...)
			buf = append(buf, `","UserAction":"`...)
			buf = append(buf, value.userAction...)
			buf = append(buf, `","DevAction":"`...)
			buf = append(buf, value.devAction...)
			buf = append(buf, `"},`...)
		}
		buf = buf[:len(buf)-1] // Remove trailing comma
	}

	buf = append(buf, "}}"...)
	return
}

func (e *Error) LenAsJSON() (ln int) {
	ln = 38 // len(`{"ID":18446744073709551615,"Detail":{}`)
	if len(e.detail) != 0 {
		ln += len(e.detail) * 76 // 76 = 10(len(uint32)) + 66(len('{"Domain":"","Summary":"","Overview":"","UserAction":"","DevAction":"",}'))
		for _, value := range e.detail {
			ln += len(value.domain)
			ln += len(value.summary)
			ln += len(value.overview)
			ln += len(value.userAction)
			ln += len(value.devAction)
		}
	}
	return ln
}

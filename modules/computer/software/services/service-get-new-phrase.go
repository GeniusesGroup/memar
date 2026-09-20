/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

import (
	"libgo/authorization"
	er "libgo/error"
	"libgo/http"
	"libgo/json"
	lang "libgo/language"
	"libgo/srpc"
	"libgo/syllab"
)

var getNewPhraseCaptchaService = service.Service{
	URN:                "domain/captcha.protocol.service; name=get-new-phrase-captcha",
	Domain:             DomainName,
	ID:                 4545477414109050749,
	IssueDate:          1593013452,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Authorization: authorization.Service{
		CRUD:     authorization.CRUDRead,
		UserType: protocol.UserType_All,
	},

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "GetNewPhraseCaptcha",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "returns new phrase captcha challenge that expire in 4 minute",
	},
	TAGS: []string{
		"Authentication",
	},

	SRPCHandler: GetNewPhraseCaptchaSRPC,
	ServeHTTP: GetNewPhraseCaptchaHTTP,
}

// GetNewPhraseCaptchaSRPC is sRPC handler of GetNewPhraseCaptcha service.
func GetNewPhraseCaptchaSRPC(st protocol.Stream) {
	var req = &getNewPhraseCaptchaReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	var res = &getNewPhraseCaptchaRes{}
	res, err = getNewPhraseCaptcha(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		return
	}

	st.OutcomePayload = make([]byte, srpc.MinLength+res.LenAsSyllab())
	res.ToSyllab(srpc.GetPayload(st.OutcomePayload))
}

// GetNewPhraseCaptchaHTTP is HTTP handler of GetNewPhraseCaptcha service.
func GetNewPhraseCaptchaHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &getNewPhraseCaptchaReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	var res = &getNewPhraseCaptchaRes{}
	res, err = getNewPhraseCaptcha(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
	httpRes.SetBody(json.NewCodec(res))
}

type getNewPhraseCaptchaReq struct {
	Language    protocol.Language
	ImageFormat ImageFormat
}

type getNewPhraseCaptchaRes struct {
	CaptchaID [16]byte `json:",string"`
	Image     []byte   `json:",string"`
}

func getNewPhraseCaptcha(st protocol.Stream, req *getNewPhraseCaptchaReq) (res *getNewPhraseCaptchaRes, err protocol.Error) {
	var pc *PhraseCaptcha = phraseCaptchas.NewImage(req.Language, req.ImageFormat)
	res = &getNewPhraseCaptchaRes{
		CaptchaID: pc.ID,
		Image:     pc.Image,
	}
	return
}

/*
	Request Encoders & Decoders
*/

func (req *getNewPhraseCaptchaReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	req.Language = protocol.Language(syllab.GetUInt8(buf, 0))
	req.ImageFormat = ImageFormat(syllab.GetUInt8(buf, 1))
	return
}

func (req *getNewPhraseCaptchaReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32){
	syllab.SetUInt32(buf, 0, uint32(req.Language))
	syllab.SetUInt8(buf, 4, uint8(req.ImageFormat))
	return
}

func (req *getNewPhraseCaptchaReq) LenOfSyllabStack() uint32 {
	return 5
}

func (req *getNewPhraseCaptchaReq) LenOfSyllabHeap() (ln uint32) {
	return
}

func (req *getNewPhraseCaptchaReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

// jsonDecoder decode minified version as {"Language":0,"ImageFormat":0}
func (req *getNewPhraseCaptchaReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "Language":
			var num uint32
			num, err = decoder.DecodeUInt32()
			req.Language = protocol.Language(num)
		case "ImageFormat":
			var num uint8
			num, err = decoder.DecodeUInt8()
			req.ImageFormat = ImageFormat(num)
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}
func (req *getNewPhraseCaptchaReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}
	encoder.EncodeString(`{"Language":`)
	encoder.EncodeUInt8(uint8(req.Language))
	encoder.EncodeString(`,"ImageFormat":`)
	encoder.EncodeUInt8(uint8(req.ImageFormat))
	encoder.EncodeByte('}')
	return encoder.Buf
}

func (req *getNewPhraseCaptchaReq) LenAsJSON() (ln int) {
	ln = 34
	return
}

/*
	Response Encoders & Decoders
*/

func (res *getNewPhraseCaptchaRes) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < res.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(res.CaptchaID[:], buf[0:])
	res.Image = syllab.UnsafeGetByteArray(buf, 16)
	return
}

func (res *getNewPhraseCaptchaRes) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32)
	copy(buf[0:], res.CaptchaID[:])
	heapIndex = syllab.SetByteArray(buf, res.Image, 16, heapIndex)
	return
}

func (res *getNewPhraseCaptchaRes) LenOfSyllabStack() uint32 {
	return 24
}

func (res *getNewPhraseCaptchaRes) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(res.Image))
	return
}

func (res *getNewPhraseCaptchaRes) LenAsSyllab() uint64 {
	return uint64(res.LenOfSyllabStack() + res.LenOfSyllabHeap())
}

func (res *getNewPhraseCaptchaRes) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "CaptchaID":
			err = decoder.DecodeByteArrayAsBase64(res.CaptchaID[:])
		case "Image":
			res.Image, err = decoder.DecodeByteSliceAsBase64()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (res *getNewPhraseCaptchaRes) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"CaptchaID":"`)
	encoder.EncodeByteSliceAsBase64(res.CaptchaID[:])

	encoder.EncodeString(`","Image":"`)
	encoder.EncodeByteSliceAsBase64(res.Image)

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (res *getNewPhraseCaptchaRes) LenAsJSON() (ln int) {
	ln = ((len(res.Image)*8 + 5) / 6)
	ln += 49
	return
}

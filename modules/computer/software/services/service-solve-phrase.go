/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

import (
	"libgo/achaemenid"
	er "libgo/error"
	"libgo/http"
	"libgo/json"
	lang "libgo/language"
	"libgo/srpc"
	"libgo/syllab"
)

var solvePhraseCaptchaService = service.Service{
	URN:                "domain/captcha.protocol.service; name=solve-phrase",
	Domain:             DomainName,
	ID:                 9691811950642900337,
	URI:                "", // API services can set like "/m?9691811950642900337" but it is not efficient, find services by ID.
	IssueDate:          1593013968,
	ExpiryDate:         0,
	ExpireInFavorOfURN: "",
	ExpireInFavorOfID:  0,
	Status:             protocol.Software_PreAlpha,

	Name: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: "SolvePhraseCaptcha",
	},
	Description: map[protocol.LanguageID]string{
		protocol.LanguageEnglish: `Solve the number captcha by give specific ID and answer
and use captcha ID for any request need it until captcha expire in 2 minute`,
	},
	TAGS: []string{
		"Authentication",
	},

	SRPCHandler: SolvePhraseCaptchaSRPC,
	ServeHTTP: SolvePhraseCaptchaHTTP,
}

// SolvePhraseCaptchaSRPC is sRPC handler of SolvePhraseCaptcha service.
func SolvePhraseCaptchaSRPC(st protocol.Stream) {
	var req = &solvePhraseCaptchaReq{}
	err = req.FromSyllab(srpc.GetPayload(st.IncomePayload))
	if err != nil {
		return
	}

	err = solvePhraseCaptcha(st, req)
}

// SolvePhraseCaptchaHTTP is HTTP handler of SolvePhraseCaptcha service.
func SolvePhraseCaptchaHTTP(st protocol.Stream, httpReq *http.Request, httpRes *http.Response) {
	var req = &solvePhraseCaptchaReq{}
	err = req.FromJSON(httpReq.Body().Marshal())
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	err = solvePhraseCaptcha(st, req)
	// Check if any error occur in bussiness logic
	if err != nil {
		httpRes.SetStatus(http.StatusBadRequestCode, http.StatusBadRequestPhrase)
		return
	}

	httpRes.SetStatus(http.StatusOKCode, http.StatusOKPhrase)
}

type solvePhraseCaptchaReq struct {
	CaptchaID [16]byte `json:",string"`
	Answer    string
}

func solvePhraseCaptcha(st protocol.Stream, req *solvePhraseCaptchaReq) (err protocol.Error) {
	err = phraseCaptchas.Solve(req.CaptchaID, req.Answer)
	return
}

/*
	Request Encoders & Decoders
*/

func (req *solvePhraseCaptchaReq) FromSyllab(payload []byte, stackIndex uint32) {
	if uint32(len(buf)) < req.LenOfSyllabStack() {
		err = syllab.ErrShortArrayDecode
		return
	}

	copy(req.CaptchaID[:], buf[0:])
	req.Answer = syllab.UnsafeGetString(buf, 16)
	return
}

func (req *solvePhraseCaptchaReq) ToSyllab(payload []byte, stackIndex, heapIndex uint32) (freeHeapIndex uint32)
	copy(buf[0:], req.CaptchaID[:])
	heapIndex = syllab.SetString(buf, req.Answer, 16, heapIndex)
	return
}

func (req *solvePhraseCaptchaReq) LenOfSyllabStack() uint32 {
	return 24
}

func (req *solvePhraseCaptchaReq) LenOfSyllabHeap() (ln uint32) {
	ln += uint32(len(req.Answer))
	return
}

func (req *solvePhraseCaptchaReq) LenAsSyllab() uint64 {
	return uint64(req.LenOfSyllabStack() + req.LenOfSyllabHeap())
}

func (req *solvePhraseCaptchaReq) FromJSON(payload []byte) (remaining []byte, err protocol.Error) {
	var decoder = json.DecoderUnsafeMinified{Buf: payload}
	for err == nil {
		var keyName = decoder.DecodeKey()
		switch keyName {
		case "CaptchaID":
			err = decoder.DecodeByteArrayAsBase64(req.CaptchaID[:])
		case "Answer":
			req.Answer, err = decoder.DecodeString()
		default:
			err = decoder.NotFoundKeyStrict()
		}

		if decoder.End() {
			return
		}
	}
	return
}

func (req *solvePhraseCaptchaReq) ToJSON(payload []byte) (added []byte, err protocol.Error) {
	var encoder = json.Encoder{Buf: payload}

	encoder.EncodeString(`{"CaptchaID":"`)
	encoder.EncodeByteSliceAsBase64(req.CaptchaID[:])

	encoder.EncodeString(`","Answer":"`)
	encoder.EncodeString(req.Answer)

	encoder.EncodeString(`"}`)
	return encoder.Buf
}

func (req *solvePhraseCaptchaReq) LenAsJSON() (ln int) {
	ln = len(req.Answer)
	ln += 50
	return
}

/* For license and copyright information please see the LEGAL file in the code repository */

package captcha

import (
	"bytes"
	"image"
	"image/draw"
	"image/jpeg"
	"image/png"
	"math/rand"
	"strconv"
	"sync"
	"time"

	"github.com/golang/freetype"
	"github.com/golang/freetype/truetype"
	"golang.org/x/image/font/gofont/gobolditalic"

	"libgo/convert"
	"libgo/log"
	"libgo/protocol"
	"libgo/time/monotonic"
	uuid "libgo/uuid/16byte"
)

// PhraseCaptchas store
type PhraseCaptchas struct {
	Len            uint8             // Number of captcha solution. can't be more than 16!
	Difficulty     uint8             // 0:very-easy, 1:easy, 2:medium, 3:hard, 4:very-hard, 5:extreme-hard
	Type           uint8             // 0:Number(625896), 1:Word(A19Cat), 2:Math(+ - * /),
	Duration       protocol.Duration // The number of seconds indicate expiration time of captchas
	ImageSize      image.Point       // Standard width & height of a captcha image.
	font           *truetype.Font
	rand           rand.Source
	mutex          sync.Mutex
	pool           map[uuid.UUID]*PhraseCaptcha
	shutdownSignal chan struct{}
}

// PhraseCaptcha store
type PhraseCaptcha struct {
	ID       uuid.UUID
	Answer   string
	ExpireIn monotonic.Time
	Status   Status
	Image    []byte // In requested lang & format
	Audio    []byte // In requested lang & format
}

// InitDefaults use to initialize phrase captchas with defaults values!
func (pcs *PhraseCaptchas) InitDefaults() (err error) {
	*pcs = PhraseCaptchas{
		Len:        6,
		Difficulty: 2,
		Type:       0,
		Duration:   120 * monotonic.Second, // 2 Minute
		ImageSize:  image.Point{128, 64},
		pool:       make(map[uuid.UUID]*PhraseCaptcha, 1024),
		rand:       rand.NewSource(time.Now().UnixNano()),
	}
	pcs.font, err = freetype.ParseFont(gobolditalic.TTF)
	if err != nil {
		// Almost never occur!
		return
	}

	// cleaner for expired captchas.
	go pcs.expirationProcessing()
	return
}

func (pcs *PhraseCaptchas) Shutdown() (alreadyStopped bool) {
	if pcs.shutdownSignal == nil {
		return true
	}
	select {
	case pcs.shutdownSignal <- struct{}{}:
	default:
		alreadyStopped = true
	}

	return
}

// NewImage make, store and return new captcha!
func (pcs *PhraseCaptchas) NewImage(lang protocol.LanguageID, imageFormat ImageFormat) (pc *PhraseCaptcha) {
	pc = &PhraseCaptcha{
		Status: Status_Created,
	}
	pc.ExpireIn.Now()
	pc.ExpireIn.Add(pcs.Duration)
	pc.ID.New()

	switch pcs.Type {
	case 0:
		pc.Answer = pcs.randomDigits()
	case 1:
		pc.Answer = pcs.randomWord(lang)
	case 2:
		pc.Answer = pcs.randomMath()
	}
	pc.Image = pcs.createImage(pc.Answer, imageFormat)

	pcs.savePhraseCaptcha(pc)
	return
}

// GetAudio return exiting captcha with audio generated if exits otherwise returns nil!
func (pcs *PhraseCaptchas) GetAudio(captchaID [16]byte, lang protocol.LanguageID, audioFormat AudioFormat) (pc *PhraseCaptcha) {
	pc = pcs.pool[captchaID]
	if pc == nil {
		return nil
	}
	pc.Audio = pcs.createAudio(pc.Answer, audioFormat)
	return
}

// Get return exiting captcha if exits otherwise returns nil!
func (pcs *PhraseCaptchas) Get(captchaID [16]byte) (pc *PhraseCaptcha) {
	pc = pcs.pool[captchaID]
	if pc != nil {
		pc.Image = nil
		pc.Audio = nil
		if pc.ExpireIn.PassNow() {
			return nil
		}
	}
	return
}

// Solve check given answer
func (pcs *PhraseCaptchas) Solve(captchaID [16]byte, answer string) protocol.Error {
	var pc *PhraseCaptcha = pcs.pool[captchaID]
	if pc == nil {
		return &ErrNotFound
	}
	pc.Image = nil
	pc.Audio = nil
	if pc.ExpireIn.PassNow() {
		return &ErrExpired
	}
	if pc.Answer != answer {
		pc.Status = Status_LastAnswerNotValid
		return &ErrAnswerNotValid
	}
	// Give more time to user to complete any process need captcha!
	pc.ExpireIn.Add(pcs.Duration)
	pc.Status = Status_Solved
	return nil
}

// Check return true if captcha exits and solved otherwise returns false!
func (pcs *PhraseCaptchas) Check(captchaID [16]byte) protocol.Error {
	var pc *PhraseCaptcha = pcs.pool[captchaID]
	if pc == nil {
		return &ErrNotFound
	}
	pc.Image = nil
	pc.Audio = nil
	if pc.ExpireIn.PassNow() {
		return &ErrExpired
	}
	if pc.Status != Status_Solved {
		return &ErrNotSolved
	}
	return nil
}

func (pcs *PhraseCaptchas) savePhraseCaptcha(pc *PhraseCaptcha) {
	pcs.mutex.Lock()
	pcs.pool[pc.ID] = pc
	pcs.mutex.Unlock()
}

func (pcs *PhraseCaptchas) randomDigits() (digits string) {
	var rand = pcs.rand.Int63()
	// TODO::: can improve performance by make below function as internal method with care about max length!
	digits = strconv.FormatInt(rand, 10)
	return digits[:pcs.Len]
}

const (
	letterIdxBits = 6                    // 6 bits to represent a letter index
	letterIdxMask = 1<<letterIdxBits - 1 // All 1-bits, as many as letterIdxBits
)
const englishLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789-"

func (pcs *PhraseCaptchas) randomWord(lang protocol.LanguageID) string {
	var b = make([]byte, pcs.Len)
	var i uint8
	for i = 0; i < pcs.Len; i++ {
		var random = pcs.rand.Int63()
		if idx := int(random & letterIdxMask); idx < len(englishLetters) {
			b[i] = englishLetters[idx]
		}
		random >>= letterIdxBits
	}
	return convert.UnsafeByteSliceToString(b)
}

func (pcs *PhraseCaptchas) randomMath() string {
	// TODO:::
	return ""
}

func (pcs *PhraseCaptchas) createImage(answer string, imageFormat ImageFormat) []byte {
	var img = image.NewRGBA(image.Rect(0, 0, pcs.ImageSize.X, pcs.ImageSize.Y))
	draw.Draw(img, img.Bounds(), image.White, image.Point{}, draw.Src)

	// TODO::: Difficulty??!!
	var c = freetype.NewContext()
	var point = freetype.Pt(10, 10+int(c.PointToFixed(24)>>6))
	c.SetDst(img)
	c.SetSrc(image.Black) //(image.NewUniform(color.RGBA{200, 100, 0, 255}))
	c.SetFont(pcs.font)
	c.SetFontSize(24)
	c.SetDPI(72)
	c.SetClip(img.Bounds())
	c.DrawString(answer, point)

	var buf bytes.Buffer
	switch imageFormat {
	case ImageFormatPNG:
		png.Encode(&buf, img)
	case ImageFormatJPEG:
		jpeg.Encode(&buf, img, &jpeg.Options{Quality: jpeg.DefaultQuality})
	}
	return buf.Bytes()
}

func (pcs *PhraseCaptchas) createAudio(answer string, audioFormat AudioFormat) []byte {
	return []byte{}
}

func (pcs *PhraseCaptchas) expirationProcessing() {
	var ticker = time.NewTicker(time.Duration(pcs.Duration))
	defer ticker.Stop()
	for {
		select {
		case <-pcs.shutdownSignal:
			return
		case <-ticker.C:
			if len(pcs.pool) != 0 {
				if protocol.AppMode_Dev {
					protocol.App.Log(log.InfoEvent(domainLog, "Cron - Idle captchas timeout free process begin...\n"+
						"Number of active captchas before free process:"+pcs.lenAsString()))
				}

				pcs.mutex.Lock()

				// Usually this process is less than one second, so get time once for compare.
				var timeNow = monotonic.Now()
				for _, captcha := range pcs.pool {
					if captcha.ExpireIn.Pass(timeNow) {
						delete(pcs.pool, captcha.ID)
					}
				}

				pcs.mutex.Unlock()

				if protocol.AppMode_Dev {
					protocol.App.Log(log.InfoEvent(domainLog, "Cron - Number of active captchas after free process:"+pcs.lenAsString()+
						"\nIdle captchas timeout free process end now!"))
				}
			}
		}
	}
}

func (pcs *PhraseCaptchas) lenAsString() string {
	// len(pcs.pool)
	return ""
}

// https://github.com/search?l=Go&q=captcha&type=Repositories
// https://github.com/dchest/captcha
// https://github.com/afocus/captcha
// https://github.com/steambap/captcha
// https://github.com/lifei6671/gocaptcha
// https://www.hcaptcha.com/

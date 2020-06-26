import {Component, ElementRef, OnDestroy, OnInit, ViewChild} from "@angular/core";
import * as imagePicker from "nativescript-imagepicker";
import {TNSHttpFormData, TNSHttpFormDataParam, TNSHttpFormDataResponse} from "nativescript-http-formdata";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "~/app/auth/auth.service";
import {UrlService} from "~/app/shared/url.service";
import {Subscription} from "rxjs";
import {TextView} from "ui/text-view";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {RouterExtensions} from "nativescript-angular/router";
import {ActivatedRoute} from "@angular/router";
import {PlantletService} from "~/app/plantlet/plantlet.service";

declare var android: any;

@Component({
    selector: "ns-post",
    templateUrl: "./post.component.html",
    styleUrls: ["./post.component.scss"],
    moduleId: module.id
})

export class PostComponent implements OnInit, OnDestroy{
    imageAddress: string;
    isLoading = false;

    private accessToken: string;
    private user_id;
    private imageName: string;

    private imageItem: any;
    private authSub: Subscription;

    @ViewChild("desc") description: ElementRef<TextView>;
    form: FormGroup;

    constructor(private http: HttpClient,
                private authService: AuthService,
                private urlService: UrlService,
                private router: RouterExtensions,
                private active: ActivatedRoute,
                private plantletService: PlantletService) {}

    ngOnInit(): void {
        this.form = new FormGroup({
            description: new FormControl(null, {validators: [Validators.required]}),
        });

        this.authSub = this.authService.user.subscribe(
            resData => {
                this.accessToken = resData["_accessToken"];
                this.user_id = resData["id"];

            }
        );
    }

    onSelectPicture() {
        let that = this;
        let context = imagePicker.create({
            mode: "single"
        });
        context.authorize().then(
            () => {
                return context.present();
            }
        ).then(
            (selection) => {
                this.imageAddress = selection[0]["_android"];
                let file: string = selection[0]["_android"];
                this.imageName = file.substr(file.lastIndexOf("/") + 1);
                this.imageItem = selection[0];
            }).catch(e => {
            console.log(e);
        });
    }

    onAddPost() {
        this.isLoading = true;
        this.addPostData();

        setTimeout(() => {
            this.addPostImage();
        }, 3000);

        setTimeout(() => {
            this.plantletService.fetchPosts('all').subscribe();
            this.isLoading = false;
            this.router.backToPreviousPage();
        }, 3000);
    }

    addPostData() {
        const desc = this.form.get('description').value.toString();

        const date = new Date().toString();
        const dateArray = date.split(" ");
        const newDate = dateArray[2] + "/" + dateArray[1] + "/" + dateArray[3] + " " + dateArray[4];

        let headers = new HttpHeaders();
        headers = headers.set('Authorization', `Bearer ${this.accessToken}`);
        let image = "null"
        if(this.imageName) {
            image = this.imageName.split('.').pop();
        }

        this.http.post(
            this.urlService.url + "/post",
            {
                "description": desc,
                "likes": 0,
                "dis_likes": 0,
                "post_image": image,
                "post_date": newDate
            },
            {
                headers: headers
            }
        ).subscribe(
            resData => {
                console.log(resData["message"]);
            }, error => {
                console.log(error['message']);
            }
        );
    }

    addPostImage() {
        if(this.imageItem) {
            this.imageItem.getImageAsync(async (image, error) => {
                let fd = new TNSHttpFormData();
                let params = [];
                let imageData: any;
                if(image) {
                    // @ts-ignore
                    let bitMapImage: android.graphics.Bitmap = image;
                    // @ts-ignore
                    let stream = new java.io.ByteArrayOutputStream();
                    bitMapImage.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, stream);
                    let byteArray = stream.toByteArray();
                    bitMapImage.recycle();

                    imageData = byteArray;
                }
                let param: TNSHttpFormDataParam = {
                    data: imageData,
                    contentType: 'image/png',
                    fileName: this.imageName,
                    parameterName: 'image'
                };
                params.push(param);
                try {
                    const response: TNSHttpFormDataResponse = await fd.post(
                        this.urlService.url + "/upload/post",
                        params,
                        {
                            headers: {
                                "Authorization": `Bearer ${this.accessToken}`
                            }
                        }
                    );
                }
                catch (e) {
                    console.log(e);
                }
            });
        }
    }

    ngOnDestroy(): void {
        this.authSub.unsubscribe();
    }
}

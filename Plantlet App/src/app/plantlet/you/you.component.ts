import {Component, OnDestroy, OnInit} from "@angular/core";
import {PlantletService} from "~/app/plantlet/plantlet.service";
import {PostDetailModel} from "~/app/plantlet/community/postDetail.model";
import {ICON_DISLIKE, ICON_LIKE, ICON_MENU, ICON_DELETE} from "~/app/plantlet/community/community.component";
import {Subscription} from "rxjs";
import {RouterExtensions} from "nativescript-angular/router";
import {SelectedIndexChangedEventData, ValueList} from "nativescript-drop-down";
import {AuthService} from "~/app/auth/auth.service";

@Component({
    selector: 'ns-you',
    templateUrl: './you.component.html',
    styleUrls: ['./you.component.scss'],
    moduleId: module.id
})

export class YouComponent implements OnInit, OnDestroy{
    isEditMode: boolean = false;
    colSpan: number = 3;
    lblColor: string = "black";

    public postDetail: PostDetailModel[] = [];
    public user: string;
    public imageText: string;

    public iconLike = ICON_LIKE;
    public iconDisLike = ICON_DISLIKE;
    public iconMenu = ICON_MENU;
    public iconDelete = ICON_DELETE;

    postSub: Subscription;
    authSub: Subscription;

    public selectedIndex: number = null;
    public items: ValueList<string>;

    constructor(private plantletService: PlantletService,
                private router: RouterExtensions,
                private authService: AuthService) {
        this.items = new ValueList<string>();
        this.items.push({
            value: `I_edit`,
            display: `edit`,
        });
        this.items.push({
            value: `I_delete`,
            display: `delete`,
        });
    }


    public onchange(args: SelectedIndexChangedEventData) {
        console.log(`Drop Down selected index changed from ${args.oldIndex} to ${args.newIndex}. New value is "${this.items.getValue(
            args.newIndex)}"`);
    }

    public onopen() {
        console.log("Drop Down opened.");
    }

    public onclose() {
        console.log("Drop Down closed.");
    }

    ngOnInit(): void {
        this.authSub = this.authService.user.subscribe(resData => {
            this.user = resData["username"];
            this.imageText = this.user[0].toUpperCase();
            console.log(resData["id"]);
            this.postSub = this.plantletService.posts.subscribe(
                res => {
                    this.postDetail = res.posts.filter(p => p["username"] === resData["username"]);
                    console.log("resData:", this.postDetail);
                }
            );
        })
    }

    onEdit() {
        this.isEditMode = !this.isEditMode;
        if(this.isEditMode == true) {
            this.colSpan = 2;
            this.lblColor = "white";
        } else {
            this.colSpan = 3;
            this.lblColor = "black";
        }
    }

    onDelete(id: number) {
        this.plantletService.deletePost(id).subscribe(resData => {

            this.plantletService.fetchPosts('list').subscribe(rest => {
                alert(resData["message"]);
                this.plantletService.posts.subscribe(ress => {
                    this.postDetail = ress.posts;
                })
            })
        })
    }

    onCancel() {
        this.isEditMode = false;
        this.colSpan = 3;
        this.lblColor = "black";
    }

    onAddPost() {
        this.router.navigate(['plantlet/post']);
    }

    ngOnDestroy(): void {
        if(this.postSub) {
            this.postSub.unsubscribe();
        }
    }



}

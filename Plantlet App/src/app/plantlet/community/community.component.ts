import {Component, OnDestroy, OnInit} from "@angular/core";
import {RouterExtensions} from "nativescript-angular/router";
import {PlantletService} from "~/app/plantlet/plantlet.service";
import {PostDetailModel} from "~/app/plantlet/community/postDetail.model";
import {Subscription} from "rxjs";

export const ICON_LIKE = String.fromCharCode(0xf164);
export const ICON_DISLIKE = String.fromCharCode(0xf165);
export const ICON_MENU = String.fromCharCode(0xf141);
export const ICON_DELETE = String.fromCharCode(0xf1f8);

@Component({
    selector: 'ns-community',
    templateUrl: './community.component.html',
    styleUrls: ['./community.component.scss'],
    moduleId: module.id
})

export class CommunityComponent implements OnInit, OnDestroy{
    public postDetail: PostDetailModel[] = [];

    public iconLike = ICON_LIKE;
    public iconDisLike = ICON_DISLIKE;

    postSub: Subscription;

    constructor(private router: RouterExtensions,
                private plantletService: PlantletService) {}

    ngOnInit(): void {
        this.postSub = this.plantletService.posts.subscribe(
            resData => {
                this.postDetail = resData.posts;
            }
        );
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

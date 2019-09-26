using Microsoft.EntityFrameworkCore.Migrations;

namespace VCAuthn.Migrations
{
    public partial class addpresentationrequest : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "ProofRequest",
                table: "Sessions",
                nullable: true);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "ProofRequest",
                table: "Sessions");
        }
    }
}
